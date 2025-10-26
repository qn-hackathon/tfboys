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
from app.services.video_client import get_video_client, init_video_client
from app.config import settings
from shared.clients import get_redis_client, init_redis_client
from shared.models import Scene
from shared.enums import TaskStatus, TTSVoice

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
    
    Note:
        客户端初始化在 Celery Worker 启动时已完成 (celery_app.py)
    """
    logger.info(f"Starting process_novel_task for task_id: {task_id}")
    
    # 获取或创建事件循环,避免使用 asyncio.run() 导致事件循环关闭
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_process_novel_task_async(task_id, novel_text))

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
    # 获取 Redis 客户端
    redis_client = get_redis_client()
    if not redis_client:
        raise RuntimeError("Redis client not initialized")

    try:
        logger.info(f"Task {task_id}: Starting async processing")

        # === 步骤1: 文本分析 ===
        await redis_client.update_task_status(task_id, TaskStatus.ANALYZING.value)
        await _update_current_stage(task_id, "正在分析小说文本")
        logger.info(f"Task {task_id}: Analyzing novel text...")
        
        scenes_data = await text_analyzer.analyze_novel(novel_text)
        total_scenes = len(scenes_data)
        
        logger.info(f"Task {task_id}: Analyzed {total_scenes} scenes")
        await _update_task_progress(task_id, "analyzing", total_scenes, 0)
        
        if total_scenes == 0:
            raise ValueError("No scenes extracted from novel text")
        
        # === 步骤2: 场景处理 ===
        await redis_client.update_task_status(task_id, TaskStatus.GENERATING_IMAGES.value)
        await _update_current_stage(task_id, "正在生成场景图像")
        logger.info(f"Task {task_id}: Generating scenes...")
        
        scenes = []
        for idx, scene_data in enumerate(scenes_data):
            scene_id = f"scene_{task_id}_{idx:03d}"
            
            logger.info(f"Task {task_id}: Processing scene {idx + 1}/{total_scenes}")
            
            # 2.1 生成场景图
            scene_image_url = await image_generator.generate_scene_image(
                scene_description=scene_data['description'],
                scene_id=scene_id
            )
            
            # 2.2 生成配音
            await redis_client.update_task_status(task_id, TaskStatus.GENERATING_AUDIO.value)
            await _update_current_stage(task_id, f"正在生成配音 ({idx + 1}/{total_scenes})")
            audio_url, audio_duration = await voice_generator.generate_voice(
                text=scene_data["narration"],
                task_id=task_id,
                scene_id=scene_id,
                voice=TTSVoice.FEMALE
            )
            
            # 2.3 构建 Scene 对象
            scene = Scene(
                scene_id=scene_id,
                scene_index=idx,
                description=scene_data["description"],
                narration=scene_data["narration"],
                subtitle_text=scene_data["narration"],  # 使用旁白作为字幕
                image_url=scene_image_url,
                audio_url=audio_url,
                duration=audio_duration
            )
            scenes.append(scene)
            
            # 更新进度
            await _update_task_progress(task_id, "processing", total_scenes, idx + 1)
            logger.info(f"Task {task_id}: Scene {idx + 1}/{total_scenes} completed")
        
        # === 步骤3: 提交视频服务 ===
        await redis_client.update_task_status(task_id, TaskStatus.SYNTHESIZING_VIDEO.value)
        await _update_current_stage(task_id, "正在合成视频")
        logger.info(f"Task {task_id}: Submitting to video service...")

        video_client = get_video_client()
        if not video_client:
            raise RuntimeError("Video client not initialized")

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
            "total_scenes": total_scenes
        }
        
    except Exception as e:
        logger.error(f"Task {task_id}: Processing failed - {str(e)}", exc_info=True)
        await redis_client.update_task_status(
            task_id,
            TaskStatus.FAILED.value,
            error=str(e)
        )
        raise




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
    redis_client = get_redis_client()
    if not redis_client:
        logger.warning(f"Task {task_id}: Redis client not initialized, skipping progress update")
        return

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


async def _update_current_stage(task_id: str, stage: str) -> None:
    """
    更新当前执行阶段

    Args:
        task_id: 任务ID
        stage: 当前阶段描述
    """
    redis_client = get_redis_client()
    if not redis_client:
        return

    try:
        task_data = await redis_client.get_task(task_id)
        if task_data:
            task_data["current_stage"] = stage
            await redis_client.save_task(task_id, task_data)
    except Exception as e:
        logger.warning(f"Task {task_id}: Failed to update current stage - {str(e)}")
