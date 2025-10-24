"""
任务数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from shared.enums import TaskStatus
from .scene import Scene


class TaskProgress(BaseModel):
    """任务进度"""
    current_step: str = Field(..., description="当前步骤")
    total_scenes: int = Field(default=0, description="总场景数")
    processed_scenes: int = Field(default=0, description="已处理场景数")
    percentage: int = Field(default=0, description="完成百分比")


class TaskResult(BaseModel):
    """任务结果"""
    video_url: Optional[str] = Field(None, description="最终视频 URL")
    duration: Optional[float] = Field(None, description="视频时长(秒)")
    scene_count: int = Field(default=0, description="场景数量")
    character_count: int = Field(default=0, description="角色数量")


class Task(BaseModel):
    """任务模型"""
    task_id: str = Field(..., description="任务唯一标识")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    novel_text: str = Field(..., description="小说文本")
    scenes: List[Scene] = Field(default_factory=list, description="场景列表")
    progress: TaskProgress = Field(default_factory=TaskProgress, description="任务进度")
    result: Optional[TaskResult] = Field(None, description="任务结果")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    error: Optional[str] = Field(None, description="错误信息")
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return self.model_dump(mode='json')
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典创建"""
        return cls(**data)
