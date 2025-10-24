from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class VideoCompletedCallback(BaseModel):
    task_id: str
    video_url: str


@router.post("/video-completed")
async def video_completed(callback: VideoCompletedCallback):
    """视频合成完成回调"""
    return {"message": "Callback received"}
