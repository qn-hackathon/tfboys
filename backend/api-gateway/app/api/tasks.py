from fastapi import APIRouter, HTTPException
from typing import List
import httpx
from app.models.task import CreateTaskRequest, TaskResponse, ApiResponse
from app.config import settings
from shared.clients import get_redis_client

router = APIRouter()


@router.post("", response_model=ApiResponse)
async def create_task(request: CreateTaskRequest):
    """创建视频生成任务"""
    async with httpx.AsyncClient() as client:
        try:
            payload = {"novel_text": request.novel_text}
            if request.style:
                payload["style"] = request.style
            
            response = await client.post(
                f"{settings.ai_service_url}/internal/tasks",
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            return ApiResponse(
                code=0,
                message="任务创建成功",
                data={"task_id": result.get("task_id")}
            )
        except httpx.HTTPError as e:
            return ApiResponse(
                code=500,
                message=f"任务创建失败: {str(e)}",
                data=None
            )


@router.get("/{task_id}", response_model=ApiResponse)
async def get_task(task_id: str):
    """获取任务详情"""
    redis_client = get_redis_client()
    if not redis_client:
        return ApiResponse(
            code=500,
            message="Redis 客户端未初始化",
            data=None
        )

    task_data = await redis_client.get_task(task_id)
    if not task_data:
        return ApiResponse(
            code=404,
            message="任务不存在",
            data=None
        )
    
    return ApiResponse(
        code=0,
        message="success",
        data=task_data
    )


@router.get("", response_model=ApiResponse)
async def list_tasks():
    """获取任务列表"""
    redis_client = get_redis_client()
    if not redis_client:
        return ApiResponse(
            code=500,
            message="Redis 客户端未初始化",
            data=None
        )

    tasks = await redis_client.list_tasks()
    return ApiResponse(
        code=0,
        message="success",
        data=tasks
    )


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
