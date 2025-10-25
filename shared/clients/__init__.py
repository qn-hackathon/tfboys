"""
共享客户端模块
"""
from .redis_client import RedisClient, redis_client, init_redis_client
from .local_storage_client import LocalStorageClient, local_storage_client, init_local_storage_client

__all__ = [
    "RedisClient",
    "redis_client",
    "init_redis_client",
    "LocalStorageClient",
    "local_storage_client",
    "init_local_storage_client",
]
