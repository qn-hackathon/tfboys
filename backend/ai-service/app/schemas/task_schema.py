"""
任务相关 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from shared.enums import TaskStatus
from shared.models import Scene


class TaskCreateRequest(BaseModel):
    """任务创建请求"""
    task_id: Optional[str] = Field(None, description="任务ID，如果不提供则自动生成")
    novel_text: str = Field(..., description="小说文本")
    style: Optional[str] = Field(None, description="视频风格")


class TaskStatusResponse(BaseModel):
    """任务状态响应"""
    task_id: str = Field(..., description="任务ID")
    status: TaskStatus = Field(..., description="任务状态")
    progress: dict = Field(default_factory=dict, description="任务进度")
    scenes: List[Scene] = Field(default_factory=list, description="场景列表")
    result: Optional[dict] = Field(None, description="任务结果")
    error: Optional[str] = Field(None, description="错误信息")


class VideoCallbackRequest(BaseModel):
    """视频合成完成回调请求"""
    task_id: str = Field(..., description="任务ID")
    video_url: str = Field(..., description="视频 URL")
    duration: float = Field(..., description="视频时长(秒)")
    status: str = Field(..., description="状态: success 或 failed")
    aspect_ratio: Optional[str] = Field(None, description="视频宽高比")
    file_size: Optional[str] = Field(None, description="视频文件大小")
    error: Optional[str] = Field(None, description="错误信息")
