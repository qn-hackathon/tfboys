"""
阿里云 OSS 对象存储客户端
"""
import oss2
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class OSSClient:
    """阿里云 OSS 客户端"""
    
    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        endpoint: str,
        bucket_name: str
    ):
        """
        初始化 OSS 客户端
        
        Args:
            access_key_id: 阿里云 AccessKey ID
            access_key_secret: 阿里云 AccessKey Secret
            endpoint: OSS Endpoint (如: oss-cn-hangzhou.aliyuncs.com)
            bucket_name: Bucket 名称
        """
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)
    
    async def upload_file(self, file_bytes: bytes, object_key: str) -> str:
        """
        上传文件到 OSS
        
        Args:
            file_bytes: 文件字节内容
            object_key: OSS 对象键 (如: characters/char_001.jpg)
            
        Returns:
            str: 文件的公开访问 URL
        """
        try:
            self.bucket.put_object(object_key, file_bytes)
            
            url = f"https://{self.bucket_name}.{self.endpoint}/{object_key}"
            logger.info(f"File uploaded successfully: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Failed to upload file to OSS: {e}")
            raise
    
    async def download_file(self, object_key: str) -> bytes:
        """
        从 OSS 下载文件
        
        Args:
            object_key: OSS 对象键
            
        Returns:
            bytes: 文件内容
        """
        try:
            result = self.bucket.get_object(object_key)
            content = result.read()
            logger.info(f"File downloaded successfully: {object_key}")
            return content
            
        except Exception as e:
            logger.error(f"Failed to download file from OSS: {e}")
            raise
    
    async def delete_file(self, object_key: str) -> bool:
        """
        从 OSS 删除文件
        
        Args:
            object_key: OSS 对象键
            
        Returns:
            bool: 删除是否成功
        """
        try:
            self.bucket.delete_object(object_key)
            logger.info(f"File deleted successfully: {object_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete file from OSS: {e}")
            return False
    
    async def file_exists(self, object_key: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            object_key: OSS 对象键
            
        Returns:
            bool: 文件是否存在
        """
        try:
            return self.bucket.object_exists(object_key)
        except Exception as e:
            logger.error(f"Failed to check file existence: {e}")
            return False
    
    def get_public_url(self, object_key: str) -> str:
        """
        获取文件的公开访问 URL
        
        Args:
            object_key: OSS 对象键
            
        Returns:
            str: 公开访问 URL
        """
        return f"https://{self.bucket_name}.{self.endpoint}/{object_key}"


oss_client: Optional[OSSClient] = None


def init_oss_client(
    access_key_id: str,
    access_key_secret: str,
    endpoint: str,
    bucket_name: str
) -> OSSClient:
    """
    初始化全局 OSS 客户端实例
    
    使用示例:
        from shared.clients import init_oss_client, oss_client
        
        init_oss_client(
            access_key_id="your_key_id",
            access_key_secret="your_key_secret",
            endpoint="oss-cn-hangzhou.aliyuncs.com",
            bucket_name="your_bucket"
        )
        
        url = await oss_client.upload_file(file_bytes, "path/to/file.jpg")
    """
    global oss_client
    oss_client = OSSClient(access_key_id, access_key_secret, endpoint, bucket_name)
    return oss_client
