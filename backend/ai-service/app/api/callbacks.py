from fastapi import APIRouter, HTTPException
from app.schemas.task_schema import VideoCallbackRequest
from shared.clients import get_redis_client
from shared.enums import TaskStatus
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/video-completed")
async def video_completed(callback: VideoCallbackRequest):
    """
    视频合成完成回调

    接收来自 Video Service 的回调通知,更新任务状态
    """
    try:
        redis_client = get_redis_client()
        if not redis_client:
            raise HTTPException(status_code=500, detail="Redis client not initialized")

        task_data = await redis_client.get_task(callback.task_id)

        if not task_data:
            raise HTTPException(status_code=404, detail=f"Task {callback.task_id} not found")

        if callback.status == "success":
            task_data["status"] = TaskStatus.COMPLETED.value
            task_data["result"] = {
                "video_url": callback.video_url,
                "duration": callback.duration
            }
            logger.info(f"Task {callback.task_id} completed successfully")
        else:
            task_data["status"] = TaskStatus.FAILED.value
            task_data["error"] = callback.error or "Video synthesis failed"
            logger.error(f"Task {callback.task_id} failed: {callback.error}")

        await redis_client.save_task(callback.task_id, task_data)
        
        return {
            "message": "Callback processed successfully",
            "task_id": callback.task_id,
            "status": task_data["status"]
        }
        
    except Exception as e:
        logger.error(f"Failed to process video callback: {e}")
        raise HTTPException(status_code=500, detail=str(e))
