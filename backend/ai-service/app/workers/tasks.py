"""
Celery 异步任务处理模块

此模块是 AI Service 的核心任务处理器,负责编排整个视频生成流程:
1. 文本分析 - 将小说文本分割为场景
2. 角色处理 - 生成角色设定图并维护一致性
3. 场景处理 - 生成场景图像和配音
4. 视频合成 - 提交给 Video Service 进行视频合成
"""
import asyncio
import logging
from typing import List, Dict
from app.workers.celery_app import celery_app
from app.services.text_analyzer import text_analyzer
from app.services.image_generator import image_generator
from app.services.voice_generator import voice_generator
from app.services.character_manager import character_manager
from app.services.video_client import video_client, init_video_client
from app.config import settings
from shared.clients import redis_client, init_redis_client
from shared.models import Scene, Character
from shared.enums import TaskStatus

logger = logging.getLogger(__name__)


@celery_app.task(name="process_novel_task")
def process_novel_task(task_id: str, novel_text: str):
    """
    处理小说生成视频任务 (Celery 入口)
    
    Args:
        task_id: 任务唯一标识
        novel_text: 小说文本内容
        
    Returns:
        dict: 任务处理结果
    """
    logger.info(f"Starting process_novel_task for task_id: {task_id}")
    
    init_redis_client(settings.redis_url)
    init_video_client(settings.video_service_url)
    
    return asyncio.run(_process_novel_task_async(task_id, novel_text))


async def _process_novel_task_async(task_id: str, novel_text: str) -> dict:
    """
    异步处理小说生成视频任务
    
    处理流程:
    1. 文本分析 → 获取场景列表
    2. 角色处理 → 生成角色设定图 + 保存到 Redis
    3. 场景处理 → 生成场景图(--cref) + 配音
    4. 提交视频服务 → 调用 video_client
    5. 全程更新任务状态到 Redis
    
    Args:
        task_id: 任务ID
        novel_text: 小说文本
        
    Returns:
        dict: 处理结果
    """
    try:
        logger.info(f"Task {task_id}: Starting async processing")
        
        # === 步骤1: 文本分析 ===
        await redis_client.update_task_status(task_id, TaskStatus.ANALYZING.value)
        logger.info(f"Task {task_id}: Analyzing novel text...")
        
        scenes_data = text_analyzer.analyze_novel(novel_text)
        total_scenes = len(scenes_data)
        
        logger.info(f"Task {task_id}: Analyzed {total_scenes} scenes")
        await _update_task_progress(task_id, "analyzing", total_scenes, 0)
        
        if total_scenes == 0:
            raise ValueError("No scenes extracted from novel text")
        
        # === 步骤2: 角色处理 ===
        logger.info(f"Task {task_id}: Processing characters...")
        characters_map = await _process_characters(task_id, scenes_data)
        logger.info(f"Task {task_id}: Processed {len(characters_map)} characters")
        
        # === 步骤3: 场景处理 ===
        await redis_client.update_task_status(task_id, TaskStatus.GENERATING_IMAGES.value)
        logger.info(f"Task {task_id}: Generating scenes...")
        
        scenes = []
        for idx, scene_data in enumerate(scenes_data):
            scene_id = f"scene_{task_id}_{idx:03d}"
            
            logger.info(f"Task {task_id}: Processing scene {idx + 1}/{total_scenes}")
            
            # 3.1 生成场景图(使用--cref)
            main_char = scene_data["characters"][0] if scene_data["characters"] else None
            char_ref_url = None
            if main_char and main_char["name"] in characters_map:
                char_ref_url = characters_map[main_char["name"]].reference_image_url
            
            scene_image_url = await image_generator.generate_image(
                prompt=f"anime style, {scene_data['description']}",
                character_ref_url=char_ref_url,
                ar="16:9"
            )
            
            # 3.2 生成配音
            await redis_client.update_task_status(task_id, TaskStatus.GENERATING_AUDIO.value)
            audio_url = await voice_generator.generate_voice(
                text=scene_data["narration"],
                voice="zhiyan"
            )
            
            # 3.3 构建 Scene 对象
            scene_characters = [
                characters_map[c["name"]] 
                for c in scene_data["characters"] 
                if c["name"] in characters_map
            ]
            
            scene = Scene(
                scene_id=scene_id,
                scene_index=idx,
                description=scene_data["description"],
                narration=scene_data["narration"],
                characters=scene_characters,
                image_url=scene_image_url,
                audio_url=audio_url,
                duration=5.0
            )
            scenes.append(scene)
            
            # 更新进度
            await _update_task_progress(task_id, "processing", total_scenes, idx + 1)
            logger.info(f"Task {task_id}: Scene {idx + 1}/{total_scenes} completed")
        
        # === 步骤4: 提交视频服务 ===
        await redis_client.update_task_status(task_id, TaskStatus.SYNTHESIZING_VIDEO.value)
        logger.info(f"Task {task_id}: Submitting to video service...")
        
        job_id = await video_client.submit_video_synthesis_job(
            task_id=task_id,
            scenes=scenes
        )
        
        logger.info(f"Task {task_id}: Video job {job_id} submitted successfully")
        
        # 保存完整任务数据
        task_data = await redis_client.get_task(task_id)
        if task_data:
            task_data["scenes"] = [s.model_dump() for s in scenes]
            task_data["video_job_id"] = job_id
            await redis_client.save_task(task_id, task_data)
        
        logger.info(f"Task {task_id}: Processing completed successfully")
        
        return {
            "status": "success",
            "task_id": task_id,
            "video_job_id": job_id,
            "total_scenes": total_scenes,
            "total_characters": len(characters_map)
        }
        
    except Exception as e:
        logger.error(f"Task {task_id}: Processing failed - {str(e)}", exc_info=True)
        await redis_client.update_task_status(
            task_id,
            TaskStatus.FAILED.value,
            error=str(e)
        )
        raise


async def _process_characters(task_id: str, scenes_data: List[Dict]) -> Dict[str, Character]:
    """
    处理角色:生成角色设定图并保存到Redis
    
    Args:
        task_id: 任务ID
        scenes_data: 场景数据列表
        
    Returns:
        Dict[str, Character]: 角色名称到角色对象的映射
    """
    characters_map = {}
    
    for scene_data in scenes_data:
        for char_data in scene_data["characters"]:
            char_name = char_data["name"]
            
            if char_name not in characters_map:
                logger.info(f"Task {task_id}: Generating character design for '{char_name}'")
                
                # 首次出现:生成角色设定图
                char_prompt = (
                    f"anime style, character design sheet, {char_name}, "
                    f"{char_data['description']}"
                )
                char_ref_url = await image_generator.generate_image(
                    prompt=char_prompt,
                    character_ref_url=None,
                    ar="1:1"
                )
                
                # 保存角色到 Redis
                character = Character(
                    character_id=f"char_{task_id}_{char_name}",
                    name=char_name,
                    description=char_data["description"],
                    reference_image_url=char_ref_url,
                    midjourney_cref_url=char_ref_url
                )
                characters_map[char_name] = character
                
                await character_manager.save_character(
                    task_id=task_id,
                    character_name=char_name,
                    character_data=character.model_dump()
                )
                
                logger.info(f"Task {task_id}: Character '{char_name}' saved successfully")
    
    return characters_map


async def _update_task_progress(
    task_id: str, 
    step: str, 
    total: int, 
    processed: int
) -> None:
    """
    更新任务进度
    
    Args:
        task_id: 任务ID
        step: 当前步骤
        total: 总数
        processed: 已处理数量
    """
    try:
        task_data = await redis_client.get_task(task_id)
        if task_data:
            task_data["progress"] = {
                "current_step": step,
                "total_scenes": total,
                "processed_scenes": processed,
                "percentage": int(processed / total * 100) if total > 0 else 0
            }
            await redis_client.save_task(task_id, task_data)
    except Exception as e:
        logger.warning(f"Task {task_id}: Failed to update progress - {str(e)}")
