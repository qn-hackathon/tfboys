"""
共享客户端模块
"""
from .redis_client import RedisClient, redis_client
from .oss_client import OSSClient, oss_client

__all__ = ["RedisClient", "redis_client", "OSSClient", "oss_client"]
