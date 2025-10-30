import json
import redis
import httpx
import logging
from datetime import datetime
from app.workers.celery_app import celery_app
from app.services.video_composer import video_composer
from app.models.video_job import VideoJob
from app.config import settings

logger = logging.getLogger(__name__)


def get_redis_client():
    return redis.from_url(settings.redis_url, decode_responses=True)


def update_job_status_in_redis(job_id: str, status: str, **kwargs):
    r = get_redis_client()
    key = f"video_job:{job_id}"
    
    job_data = r.get(key)
    if job_data:
        job_dict = json.loads(job_data)
    else:
        job_dict = {"job_id": job_id}
    
    job_dict["status"] = status
    job_dict["updated_at"] = datetime.now().isoformat()
    
    if "progress" in kwargs:
        job_dict["progress"] = kwargs["progress"]
    if "result" in kwargs:
        job_dict["result"] = kwargs["result"]
    if "error" in kwargs:
        job_dict["error"] = kwargs["error"]
    
    r.setex(key, 86400 * 7, json.dumps(job_dict))


async def send_completion_callback(task_id: str, video_url: str, duration: float, status: str, error: str = None):
    """
    发送视频合成完成回调给AI Service
    
    Args:
        task_id: 任务ID
        video_url: 视频URL
        duration: 视频时长
        status: 状态 (success/failed)
        error: 错误信息(可选)
    """
    try:
        ai_service_url = "http://ai-service:8002"
        callback_url = f"{ai_service_url}/callbacks/video-completed"
        
        payload = {
            "task_id": task_id,
            "video_url": video_url,
            "duration": duration,
            "status": status
        }
        
        if error:
            payload["error"] = error
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(callback_url, json=payload)
            response.raise_for_status()
            logger.info(f"Successfully sent callback for task {task_id}")
            
    except Exception as e:
        logger.error(f"Failed to send callback for task {task_id}: {e}")


@celery_app.task(bind=True)
def process_video_job(self, job_data: dict):
    """
    异步处理视频合成任务
    
    Args:
        job_data: 视频任务数据
    
    Returns:
        结果字典
    """
    try:
        job = VideoJob(**job_data)
        logger.info(f"Starting video job processing for job_id: {job.job_id}, task_id: {job.task_id}")
    except Exception as e:
        logger.error(f"Failed to create VideoJob from data: {e}")
        logger.error(f"Job data: {job_data}")
        raise
    
    try:
        update_job_status_in_redis(
            job.job_id,
            "processing",
            progress={"current_scene": 0, "total_scenes": len(job.scenes)}
        )
        
        import asyncio
        try:
            # 在Celery worker中，直接使用asyncio.run()创建新的事件循环
            video_url = asyncio.run(video_composer.compose_video(job))
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                # 如果已经在事件循环中，使用 run_until_complete
                loop = asyncio.get_event_loop()
                video_url = loop.run_until_complete(video_composer.compose_video(job))
            elif "no current event loop" in str(e):
                # 如果没有事件循环，创建新的
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    video_url = loop.run_until_complete(video_composer.compose_video(job))
                finally:
                    loop.close()
            else:
                raise
        
        # 获取视频时长 (这里简化处理，实际应该从视频文件获取)
        duration = 30.0  # 默认时长，实际应该从视频文件获取
        
        update_job_status_in_redis(
            job.job_id,
            "completed",
            result={"video_url": video_url}
        )
        
        # 发送完成回调给AI Service
        try:
            asyncio.run(send_completion_callback(
                job.task_id,
                video_url,
                duration,
                "success"
            ))
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(send_completion_callback(
                    job.task_id,
                    video_url,
                    duration,
                    "success"
                ))
            elif "no current event loop" in str(e):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(send_completion_callback(
                        job.task_id,
                        video_url,
                        duration,
                        "success"
                    ))
                finally:
                    loop.close()
            else:
                raise
        
        return {"status": "completed", "video_url": video_url}
    
    except Exception as e:
        error_msg = str(e)
        update_job_status_in_redis(job.job_id, "failed", error=error_msg)
        
        # 发送失败回调给AI Service
        import asyncio
        try:
            asyncio.run(send_completion_callback(
                job.task_id,
                "",
                0.0,
                "failed",
                error_msg
            ))
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(send_completion_callback(
                    job.task_id,
                    "",
                    0.0,
                    "failed",
                    error_msg
                ))
            elif "no current event loop" in str(e):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(send_completion_callback(
                        job.task_id,
                        "",
                        0.0,
                        "failed",
                        error_msg
                    ))
                finally:
                    loop.close()
            else:
                raise
        
        raise
