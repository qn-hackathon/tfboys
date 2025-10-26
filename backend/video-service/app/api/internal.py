from fastapi import APIRouter, HTTPException
import uuid
import json
import redis
import logging
from datetime import datetime
from app.models.video_job import VideoJob, VideoJobRequest
from app.workers.tasks import process_video_job
from app.config import settings

logger = logging.getLogger(__name__)

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
    try:
        logger.info(f"Received video synthesis job request for task_id: {request.task_id}")
        logger.debug(f"Request data: task_id={request.task_id}, scenes_count={len(request.scenes) if request.scenes else 0}")
        
        # 验证请求数据
        if not request.task_id:
            logger.error("task_id is missing from request")
            raise HTTPException(status_code=422, detail="task_id is required")
        
        if not request.scenes:
            logger.error("scenes list is empty")
            raise HTTPException(status_code=422, detail="scenes list cannot be empty")
        
        # 验证每个场景的必需字段
        for i, scene in enumerate(request.scenes):
            if not scene.scene_id:
                logger.error(f"scene[{i}].scene_id is missing")
                raise HTTPException(status_code=422, detail=f"scene[{i}].scene_id is required")
            if not scene.description:
                logger.error(f"scene[{i}].description is missing")
                raise HTTPException(status_code=422, detail=f"scene[{i}].description is required")
            if not scene.narration:
                logger.error(f"scene[{i}].narration is missing")
                raise HTTPException(status_code=422, detail=f"scene[{i}].narration is required")
        
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
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create video synthesis job: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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
