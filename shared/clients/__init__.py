"""
共享客户端模块
"""
from .redis_client import RedisClient, redis_client, init_redis_client
from .local_storage_client import LocalStorageClient, local_storage_client, init_local_storage_client


def get_local_storage_client():
    """
    获取本地存储客户端实例（动态获取，解决模块导入时的值复制问题）

    Returns:
        LocalStorageClient: 本地存储客户端实例，如果未初始化则返回 None
    """
    import sys
    # 直接从 sys.modules 获取子模块
    lsc_module = sys.modules.get('shared.clients.local_storage_client')
    if lsc_module is None:
        # 如果模块未加载，先导入
        import importlib
        lsc_module = importlib.import_module('shared.clients.local_storage_client')
    return lsc_module.local_storage_client


__all__ = [
    "RedisClient",
    "redis_client",
    "init_redis_client",
    "LocalStorageClient",
    "local_storage_client",
    "init_local_storage_client",
    "get_local_storage_client",
]
