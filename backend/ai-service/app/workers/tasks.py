"""
Celery异步任务
"""
from app.workers.celery_app import celery_app
from app.services.text_analyzer import text_analyzer
from app.services.image_generator import image_generator
from app.services.voice_generator import voice_generator


@celery_app.task(name="process_novel_task")
def process_novel_task(task_id: str, novel_text: str):
    """
    处理小说文本生成任务
    
    1. 文本分析 - 分割场景
    2. 角色识别 - 提取角色
    3. 图像生成 - Midjourney
    4. 配音生成 - 阿里云TTS
    5. 调用视频服务合成
    """
    print(f"Processing task {task_id}")
    
    return {"task_id": task_id, "status": "processing"}
