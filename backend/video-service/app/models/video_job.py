from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from .scene import Scene
from .video_config import VideoConfig


class VideoResult(BaseModel):
    video_url: str
    duration: float
    file_size: int
    thumbnail_url: Optional[str] = None


class VideoJob(BaseModel):
    job_id: str
    task_id: str
    status: str
    scenes: List[Scene]
    video_config: VideoConfig
    progress: Dict = {}
    result: Optional[VideoResult] = None
    error: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class VideoJobRequest(BaseModel):
    task_id: str
    scenes: List[Scene]
    video_config: VideoConfig = VideoConfig()
