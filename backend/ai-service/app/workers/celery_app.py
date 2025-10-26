from celery import Celery
from celery.signals import worker_init, task_prerun
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
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    # 任务路由配置 - 确保AI任务只发送到AI worker
    task_routes={
        'process_novel_task': {'queue': 'ai_queue'},
    },
    task_default_queue='ai_queue',
    # Redis 客户端配置 - 修复 "wrong number of arguments for 'ping' command" 错误
    broker_transport_options={
        'visibility_timeout': 3600,
        'fanout_prefix': True,
        'fanout_patterns': True,
        'health_check_interval': 0,  # 禁用 health check 避免 ping 命令问题
    },
    result_backend_transport_options={
        'retry_policy': {
            'timeout': 5.0
        },
        'health_check_interval': 0,  # 禁用 health check 避免 ping 命令问题
    },
    # 自动发现任务模块
    imports=['app.workers.tasks'],
)


@worker_init.connect
def init_worker(**kwargs):
    """
    Celery Worker 启动时初始化客户端
    在 Worker 进程启动时执行一次
    """
    from shared.clients import init_redis_client, init_local_storage_client
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
        init_local_storage_client(base_dir="/tmp/tfboys")
        logger.info("Local storage client initialized in worker")
    except Exception as e:
        logger.error(f"Failed to initialize Local storage client in worker: {e}")

    try:
        init_video_client(settings.video_service_url)
        logger.info("Video client initialized in worker")
    except Exception as e:
        logger.error(f"Failed to initialize Video client in worker: {e}")


@task_prerun.connect
def init_task_clients(**kwargs):
    """
    每个任务执行前确保客户端已初始化
    这对于 prefork 模式的子进程很重要
    """
    from shared.clients import init_redis_client, init_local_storage_client, get_redis_client, get_local_storage_client
    from app.services.video_client import init_video_client, get_video_client
    import logging

    logger = logging.getLogger(__name__)

    # 检查并初始化 Redis 客户端
    if get_redis_client() is None:
        logger.info("Redis client not found in worker process, initializing...")
        init_redis_client(settings.redis_url)

    # 检查并初始化 Local Storage 客户端
    if get_local_storage_client() is None:
        logger.info("Local storage client not found in worker process, initializing...")
        init_local_storage_client(base_dir="/tmp/tfboys")

    # 检查并初始化 Video 客户端
    if get_video_client() is None:
        logger.info("Video client not found in worker process, initializing...")
        init_video_client(settings.video_service_url)
