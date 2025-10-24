from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import tasks, health
from app.config import settings
from shared.clients import init_redis_client
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("Initializing API Gateway...")
    
    try:
        init_redis_client(settings.redis_url)
        logger.info("Redis client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {e}")
    
    logger.info("API Gateway initialized successfully")
    
    yield
    
    logger.info("Shutting down API Gateway...")


app = FastAPI(
    title="TFBoys API Gateway",
    description="文字生成视频系统 API网关",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(health.router, tags=["health"])


@app.get("/")
def root():
    return {"message": "TFBoys API Gateway", "version": "1.0.0"}
