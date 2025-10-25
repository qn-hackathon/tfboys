"""
本地文件存储客户端 - 替代阿里云 OSS
"""
import os
import shutil
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class LocalStorageClient:
    """本地文件存储客户端"""
    
    def __init__(self, base_dir: str = "/tmp/tfboys"):
        """
        初始化本地存储客户端
        
        Args:
            base_dir: 基础存储目录 (默认: /tmp/tfboys)
        """
        self.base_dir = base_dir
        self._ensure_base_dir()
    
    def _ensure_base_dir(self):
        """确保基础目录存在"""
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Local storage initialized at: {self.base_dir}")
    
    def _get_full_path(self, object_key: str) -> str:
        """
        获取文件完整路径
        
        Args:
            object_key: 对象键 (如: characters/char_001.jpg)
            
        Returns:
            str: 文件完整路径
        """
        return os.path.join(self.base_dir, object_key)
    
    async def upload_file(self, file_bytes: bytes, object_key: str) -> str:
        """
        保存文件到本地存储
        
        Args:
            file_bytes: 文件字节内容
            object_key: 对象键 (如: characters/char_001.jpg)
            
        Returns:
            str: 文件的本地路径
        """
        try:
            full_path = self._get_full_path(object_key)
            
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'wb') as f:
                f.write(file_bytes)
            
            logger.info(f"File saved successfully: {full_path}")
            return full_path
            
        except Exception as e:
            logger.error(f"Failed to save file to local storage: {e}")
            raise
    
    async def download_file(self, object_key: str) -> bytes:
        """
        从本地存储读取文件
        
        Args:
            object_key: 对象键
            
        Returns:
            bytes: 文件内容
        """
        try:
            full_path = self._get_full_path(object_key)
            
            with open(full_path, 'rb') as f:
                content = f.read()
            
            logger.info(f"File read successfully: {full_path}")
            return content
            
        except Exception as e:
            logger.error(f"Failed to read file from local storage: {e}")
            raise
    
    async def delete_file(self, object_key: str) -> bool:
        """
        从本地存储删除文件
        
        Args:
            object_key: 对象键
            
        Returns:
            bool: 删除是否成功
        """
        try:
            full_path = self._get_full_path(object_key)
            
            if os.path.exists(full_path):
                os.remove(full_path)
                logger.info(f"File deleted successfully: {full_path}")
                return True
            else:
                logger.warning(f"File not found: {full_path}")
                return False
            
        except Exception as e:
            logger.error(f"Failed to delete file from local storage: {e}")
            return False
    
    async def file_exists(self, object_key: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            object_key: 对象键
            
        Returns:
            bool: 文件是否存在
        """
        try:
            full_path = self._get_full_path(object_key)
            return os.path.exists(full_path)
        except Exception as e:
            logger.error(f"Failed to check file existence: {e}")
            return False
    
    def get_public_url(self, object_key: str) -> str:
        """
        获取文件的本地路径 (兼容 OSS API)
        
        Args:
            object_key: 对象键
            
        Returns:
            str: 文件本地路径
        """
        return self._get_full_path(object_key)


local_storage_client: Optional[LocalStorageClient] = None


def init_local_storage_client(base_dir: str = "/tmp/tfboys") -> LocalStorageClient:
    """
    初始化全局本地存储客户端实例
    
    使用示例:
        from shared.clients import init_local_storage_client, local_storage_client
        
        init_local_storage_client(base_dir="/tmp/tfboys")
        
        path = await local_storage_client.upload_file(file_bytes, "path/to/file.jpg")
    """
    global local_storage_client
    local_storage_client = LocalStorageClient(base_dir)
    return local_storage_client
