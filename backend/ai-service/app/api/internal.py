from fastapi import APIRouter, BackgroundTasks, HTTPException
import uuid
import logging
from datetime import datetime
from app.workers.tasks import process_novel_task
from app.schemas.task_schema import TaskCreateRequest, TaskStatusResponse
from shared.clients import get_redis_client
from shared.enums import TaskStatus

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/tasks")
async def create_task(request: TaskCreateRequest, background_tasks: BackgroundTasks):
    """
    创建 AI 处理任务
    
    接收来自 API Gateway 的任务创建请求,触发 Celery 异步任务
    """
    if not request.novel_text or not request.novel_text.strip():
        raise HTTPException(status_code=400, detail="novel_text cannot be empty")
    
    if len(request.novel_text) > 50000:
        raise HTTPException(status_code=400, detail="novel_text exceeds maximum length of 50000 characters")
    
    task_id = request.task_id if hasattr(request, 'task_id') and request.task_id else str(uuid.uuid4())
    
    task_data = {
        "task_id": task_id,
        "status": TaskStatus.PENDING.value,
        "novel_text": request.novel_text,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    if request.style:
        task_data["style"] = request.style

    redis_client = get_redis_client()
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    try:
        await redis_client.save_task(task_id, task_data)
        logger.info(f"Task {task_id} saved to Redis successfully")
        
        # 提交 Celery 异步任务
        logger.info(f"Submitting Celery task for {task_id}")
        result = process_novel_task.delay(task_id, request.novel_text)
        logger.info(f"Celery task submitted successfully: {result.id}")
        
    except Exception as e:
        logger.error(f"Failed to create task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")
    
    return {
        "task_id": task_id,
        "status": TaskStatus.PENDING.value,
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    获取任务状态

    从 Redis 查询任务状态和处理进度
    """
    redis_client = get_redis_client()
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    task_data = await redis_client.get_task(task_id)
    
    if not task_data:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # Convert scene dicts to Scene objects if present
    if "scenes" in task_data and task_data["scenes"]:
        from shared.models import Scene
        task_data["scenes"] = [Scene(**s) for s in task_data["scenes"]]
    
    return TaskStatusResponse(**task_data)
