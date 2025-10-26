from fastapi import APIRouter, HTTPException
from typing import List
import httpx
from app.models.task import CreateTaskRequest, TaskResponse
from app.config import settings
from shared.clients import get_redis_client

router = APIRouter()


@router.post("", response_model=dict)
async def create_task(request: CreateTaskRequest):
    """创建视频生成任务"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ai_service_url}/internal/tasks",
                json={"novel_text": request.novel_text},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """获取任务详情"""
    redis_client = get_redis_client()
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    task_data = await redis_client.get_task(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_data


@router.get("", response_model=List[TaskResponse])
async def list_tasks():
    """获取任务列表"""
    redis_client = get_redis_client()
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    tasks = await redis_client.list_tasks()
    return tasks


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """删除任务"""
    redis_client = get_redis_client()
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    success = await redis_client.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
