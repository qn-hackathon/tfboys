from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/callbacks", tags=["callbacks"])


class VideoCompletedCallback(BaseModel):
    job_id: str
    task_id: str
    status: str
    video_url: str
    duration: float


@router.post("/video-completed")
async def video_completed_callback(callback_data: VideoCompletedCallback):
    """
    视频合成完成回调(可选)
    
    视频服务可以回调AI服务或主服务更新任务状态
    """
    return {
        "code": 0,
        "message": "回调接收成功"
    }
