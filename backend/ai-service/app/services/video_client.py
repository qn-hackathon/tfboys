"""
视频服务 HTTP 客户端
"""
import httpx
import logging
from typing import List
from shared.models import Scene
from shared.exceptions import APICallException
from app.utils.retry import retry_on_failure

logger = logging.getLogger(__name__)


class VideoClient:
    """视频服务客户端"""
    
    def __init__(self, base_url: str, timeout: int = 300):
        """
        初始化视频服务客户端
        
        Args:
            base_url: 视频服务基础 URL (如: http://video-service:8003)
            timeout: 请求超时时间(秒)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    @retry_on_failure(max_retries=3, delay=2.0, backoff=2.0)
    async def submit_video_synthesis_job(
        self,
        task_id: str,
        scenes: List[Scene]
    ) -> str:
        """
        提交视频合成任务
        
        Args:
            task_id: 任务ID
            scenes: 场景列表
            
        Returns:
            str: 任务ID
            
        Raises:
            APICallException: API 调用失败
        """
        try:
            url = f"{self.base_url}/internal/synthesize"
            
            payload = {
                "task_id": task_id,
                "scenes": [scene.model_dump() for scene in scenes]
            }
            
            logger.info(f"Submitting video synthesis job for task {task_id}")
            
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Video synthesis job submitted successfully: {result}")
            
            return result.get("task_id", task_id)
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to submit video synthesis job: {e}")
            raise APICallException("VideoService", str(e))
        except Exception as e:
            logger.error(f"Unexpected error in video synthesis submission: {e}")
            raise APICallException("VideoService", str(e))
    
    async def get_job_status(self, task_id: str) -> dict:
        """
        获取视频合成任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            dict: 任务状态
        """
        try:
            url = f"{self.base_url}/internal/status/{task_id}"
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to get video job status: {e}")
            raise APICallException("VideoService", str(e))
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


video_client: VideoClient = None


def init_video_client(base_url: str, timeout: int = 300) -> VideoClient:
    """
    初始化全局视频服务客户端实例

    使用示例:
        from app.services.video_client import init_video_client, video_client

        init_video_client("http://video-service:8003")

        await video_client.submit_video_synthesis_job(task_id, scenes)
    """
    global video_client
    video_client = VideoClient(base_url, timeout)
    return video_client


def get_video_client() -> VideoClient:
    """
    获取视频服务客户端实例（动态获取，解决模块导入时的值复制问题）

    Returns:
        VideoClient: 视频服务客户端实例，如果未初始化则返回 None
    """
    import sys
    # 直接从 sys.modules 获取模块
    vc_module = sys.modules.get('app.services.video_client')
    if vc_module is None:
        # 如果模块未加载，先导入
        import importlib
        vc_module = importlib.import_module('app.services.video_client')
    return vc_module.video_client
