from fastapi import APIRouter, BackgroundTasks, HTTPException
import uuid
from datetime import datetime
from app.workers.tasks import process_novel_task
from app.schemas.task_schema import TaskCreateRequest, TaskStatusResponse
from shared.clients import redis_client
from shared.enums import TaskStatus

router = APIRouter()


@router.post("/tasks")
async def create_task(request: TaskCreateRequest, background_tasks: BackgroundTasks):
    """
    创建 AI 处理任务
    
    接收来自 API Gateway 的任务创建请求,触发 Celery 异步任务
    """
    task_id = request.task_id if hasattr(request, 'task_id') and request.task_id else str(uuid.uuid4())
    
    task_data = {
        "task_id": task_id,
        "status": TaskStatus.PENDING.value,
        "novel_text": request.novel_text,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    if redis_client:
        await redis_client.save_task(task_id, task_data)
    
    background_tasks.add_task(process_novel_task.delay, task_id, request.novel_text)
    
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
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")
    
    task_data = await redis_client.get_task(task_id)
    
    if not task_data:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return TaskStatusResponse(**task_data)
