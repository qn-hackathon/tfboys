import json
import redis
from datetime import datetime
from app.workers.celery_app import celery_app
from app.services.video_composer import video_composer
from app.models.video_job import VideoJob
from app.config import settings


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


@celery_app.task(bind=True)
def process_video_job(self, job_data: dict):
    """
    异步处理视频合成任务
    
    Args:
        job_data: 视频任务数据
    
    Returns:
        结果字典
    """
    job = VideoJob(**job_data)
    
    try:
        update_job_status_in_redis(
            job.job_id,
            "processing",
            progress={"current_scene": 0, "total_scenes": len(job.scenes)}
        )
        
        import asyncio
        video_url = asyncio.run(video_composer.compose_video(job))
        
        update_job_status_in_redis(
            job.job_id,
            "completed",
            result={"video_url": video_url}
        )
        
        return {"status": "completed", "video_url": video_url}
    
    except Exception as e:
        error_msg = str(e)
        update_job_status_in_redis(job.job_id, "failed", error=error_msg)
        raise
