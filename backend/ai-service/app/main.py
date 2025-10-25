from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import internal, callbacks
from app.config import settings
from shared.clients import init_redis_client, init_local_storage_client
from app.services.video_client import init_video_client
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("Initializing AI Service...")
    
    try:
        init_redis_client(settings.redis_url)
        logger.info("Redis client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {e}")
    
    try:
        init_local_storage_client(base_dir="/tmp/tfboys")
        logger.info("Local storage client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize local storage client: {e}")
    
    try:
        init_video_client(settings.video_service_url)
        logger.info("Video client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Video client: {e}")
    
    logger.info("AI Service initialized successfully")
    
    yield
    
    logger.info("Shutting down AI Service...")


app = FastAPI(
    title="TFBoys AI Service",
    description="AI处理服务 - 文本分析、图像生成、配音生成",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(internal.router, prefix="/internal", tags=["internal"])
app.include_router(callbacks.router, prefix="/callbacks", tags=["callbacks"])


@app.get("/")
def root():
    return {"message": "TFBoys AI Service", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
