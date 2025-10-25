import os
import httpx
import shutil
from pathlib import Path
from urllib.parse import urlparse


class LocalStorageClient:
    def __init__(self, base_dir: str = "/tmp/tfboys"):
        self.base_dir = base_dir
        Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    async def upload_file(self, local_path: str, object_key: str) -> str:
        """
        复制文件到共享存储目录
        
        Args:
            local_path: 源文件路径
            object_key: 目标对象键
            
        Returns:
            目标文件路径
        """
        dest_path = os.path.join(self.base_dir, object_key)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        shutil.copy2(local_path, dest_path)
        return dest_path
    
    async def download_file(self, url_or_path: str, local_path: str):
        """
        从本地路径或URL下载文件
        
        Args:
            url_or_path: 源文件路径或URL (支持 http://, https://, file://, 或直接文件路径)
            local_path: 目标本地路径
        """
        if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.get(url_or_path)
                response.raise_for_status()
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
        elif url_or_path.startswith('file://'):
            file_path = urlparse(url_or_path).path
            if os.path.exists(file_path):
                shutil.copy2(file_path, local_path)
            else:
                raise FileNotFoundError(f"File not found: {url_or_path} (resolved to: {file_path})")
        else:
            if os.path.exists(url_or_path):
                shutil.copy2(url_or_path, local_path)
            else:
                raise FileNotFoundError(f"File not found: {url_or_path}")


local_storage_client = LocalStorageClient()
