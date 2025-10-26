from celery import Celery
from app.config import settings

celery_app = Celery(
    "video_service",
    broker=settings.redis_url,
    backend=settings.redis_url
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    # 任务路由配置 - 确保视频任务只发送到video worker
    task_routes={
        'process_video_job': {'queue': 'video_queue'},
    },
    task_default_queue='video_queue',
)
