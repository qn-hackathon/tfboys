from app.workers.celery_app import celery_app
import asyncio


@celery_app.task(name="process_task")
def process_task(task_id: str, novel_text: str):
    """
    处理视频生成任务
    1. 文本分析
    2. 图像生成
    3. 配音生成
    4. 发送到视频服务
    """
    print(f"Processing task {task_id}")
    
    return asyncio.run(_process_task_async(task_id, novel_text))


async def _process_task_async(task_id: str, novel_text: str):
    """异步处理任务"""
    print(f"Analyzing text for task {task_id}...")
    print(f"Text length: {len(novel_text)} characters")
    
    return {"status": "completed", "task_id": task_id}
