from pydantic import BaseModel
from typing import Optional, Union
from shared.enums import TaskStatus


class CreateTaskRequest(BaseModel):
    novel_text: str
    style: Optional[str] = None


class TaskProgress(BaseModel):
    total_scenes: int
    processed_scenes: int


class TaskResult(BaseModel):
    video_url: Optional[str] = None
    aspect_ratio: Optional[str] = None
    file_size: Optional[str] = None


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus  # 使用 shared 的 TaskStatus 枚举
    novel_text: str
    created_at: str
    progress: Optional[TaskProgress] = None
    current_stage: Optional[str] = None
    result: Optional[TaskResult] = None
    error: Optional[str] = None


class ApiResponse(BaseModel):
    """统一 API 响应格式"""
    code: int = 0
    message: str = "success"
    data: Optional[Union[dict, list, str]] = None
