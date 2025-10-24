import oss2
import httpx
from app.config import settings


class OSSClient:
    def __init__(self):
        if settings.oss_endpoint and settings.oss_access_key:
            auth = oss2.Auth(settings.oss_access_key, settings.oss_secret_key)
            self.bucket = oss2.Bucket(auth, settings.oss_endpoint, settings.oss_bucket)
        else:
            self.bucket = None
    
    async def upload_file(self, local_path: str, oss_key: str) -> str:
        if not self.bucket:
            return f"file://{local_path}"
        
        try:
            self.bucket.put_object_from_file(oss_key, local_path)
            url = f"{settings.oss_endpoint}/{settings.oss_bucket}/{oss_key}"
            return url
        except Exception as e:
            print(f"OSS upload error: {e}")
            raise
    
    async def download_file(self, url: str, local_path: str):
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(response.content)


oss_client = OSSClient()
