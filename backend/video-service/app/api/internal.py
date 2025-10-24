from fastapi import APIRouter, HTTPException
import uuid
import json
import redis
from datetime import datetime
from app.models.video_job import VideoJob, VideoJobRequest
from app.workers.tasks import process_video_job
from app.config import settings

router = APIRouter(prefix="/internal", tags=["internal"])


def get_redis_client():
    return redis.from_url(settings.redis_url, decode_responses=True)


def save_job_to_redis(job: VideoJob):
    r = get_redis_client()
    key = f"video_job:{job.job_id}"
    job_dict = job.model_dump(mode='json')
    job_dict["created_at"] = job.created_at.isoformat()
    job_dict["updated_at"] = job.updated_at.isoformat()
    r.setex(key, 86400 * 7, json.dumps(job_dict))


def get_job_from_redis(job_id: str):
    r = get_redis_client()
    key = f"video_job:{job_id}"
    job_data = r.get(key)
    if job_data:
        return json.loads(job_data)
    return None


@router.post("/video-synthesis/jobs")
async def create_video_synthesis_job(request: VideoJobRequest):
    """
    创建视频合成任务(AI服务调用)
    
    接收场景数据包,启动Celery异步任务
    """
    job_id = str(uuid.uuid4())
    
    job = VideoJob(
        job_id=job_id,
        task_id=request.task_id,
        status="pending",
        scenes=request.scenes,
        video_config=request.video_config
    )
    
    save_job_to_redis(job)
    
    job_dict = job.model_dump(mode='json')
    job_dict["created_at"] = job.created_at.isoformat()
    job_dict["updated_at"] = job.updated_at.isoformat()
    process_video_job.delay(job_dict)
    
    return {
        "code": 0,
        "message": "视频合成任务已创建",
        "data": {
            "job_id": job_id,
            "task_id": request.task_id,
            "status": "pending"
        }
    }


@router.get("/video-synthesis/jobs/{job_id}")
async def get_video_synthesis_job(job_id: str):
    """查询视频合成任务状态"""
    job = get_job_from_redis(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return {
        "code": 0,
        "message": "成功",
        "data": job
    }
