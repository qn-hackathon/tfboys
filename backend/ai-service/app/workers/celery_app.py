from celery import Celery
from celery.signals import worker_init
from app.config import settings

celery_app = Celery(
    "tfboys-ai-service",
    broker=settings.redis_url,
    backend=settings.redis_url
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@worker_init.connect
def init_worker(**kwargs):
    """
    Celery Worker 启动时初始化客户端
    在 Worker 进程启动时执行一次,避免每个任务都重复初始化
    """
    from shared.clients import init_redis_client
    from app.services.video_client import init_video_client
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info("Initializing Celery worker clients...")
    
    try:
        init_redis_client(settings.redis_url)
        logger.info("Redis client initialized in worker")
    except Exception as e:
        logger.error(f"Failed to initialize Redis client in worker: {e}")
    
    try:
        init_video_client(settings.video_service_url)
        logger.info("Video client initialized in worker")
    except Exception as e:
        logger.error(f"Failed to initialize Video client in worker: {e}")
