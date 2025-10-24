from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
import uuid

router = APIRouter()


class Scene(BaseModel):
    scene_id: str
    scene_index: int
    image_url: str
    audio_url: str
    narration: str
    duration: float


class VideoSynthesisRequest(BaseModel):
    task_id: str
    scenes: List[Scene]


@router.post("/video-synthesis/jobs")
async def create_video_synthesis_job(
    request: VideoSynthesisRequest,
    background_tasks: BackgroundTasks
):
    """创建视频合成任务"""
    job_id = str(uuid.uuid4())
    
    return {
        "job_id": job_id,
        "status": "processing"
    }


@router.get("/video-synthesis/jobs/{job_id}")
async def get_video_synthesis_job(job_id: str):
    """查询视频合成任务状态"""
    return {
        "job_id": job_id,
        "status": "completed",
        "video_url": "https://example.com/video.mp4"
    }
