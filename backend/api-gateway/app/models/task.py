from pydantic import BaseModel
from typing import Optional
from shared.enums import TaskStatus


class CreateTaskRequest(BaseModel):
    novel_text: str


class TaskProgress(BaseModel):
    total_scenes: int
    processed_scenes: int


class TaskResult(BaseModel):
    video_url: str


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus  # 使用 shared 的 TaskStatus 枚举
    novel_text: str
    created_at: str
    progress: Optional[TaskProgress] = None
    result: Optional[TaskResult] = None
    error: Optional[str] = None
