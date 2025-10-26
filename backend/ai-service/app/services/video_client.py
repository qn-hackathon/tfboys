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
        logger.info(f"VideoClient initialized with base_url: {self.base_url}, timeout: {timeout}")
    
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
            url = f"{self.base_url}/internal/video-synthesis/jobs"
            
            # 验证scenes数据
            if not scenes:
                raise ValueError("Scenes list cannot be empty")
            
            # 转换scenes数据，确保字段匹配
            scenes_data = []
            for scene in scenes:
                scene_dict = scene.model_dump()
                # 确保所有必需字段都存在
                required_fields = ['scene_id', 'scene_index', 'description', 'narration']
                for field in required_fields:
                    if field not in scene_dict:
                        raise ValueError(f"Missing required field '{field}' in scene data")
                scenes_data.append(scene_dict)
            
            payload = {
                "task_id": task_id,
                "scenes": scenes_data,
                "video_config": {
                    "resolution": "1920x1080",
                    "fps": 30,
                    "transition_effect": "fade",
                    "subtitle_style": {
                        "font_size": 32,
                        "color": "white",
                        "position": "bottom",
                        "border_width": 2,
                        "border_color": "black"
                    }
                }
            }
            
            logger.info(f"Submitting video synthesis job for task {task_id} with {len(scenes)} scenes")
            logger.debug(f"Payload: {payload}")
            
            response = await self.client.post(url, json=payload)
            
            # 记录响应状态和内容
            logger.info(f"Video service response status: {response.status_code}")
            if response.status_code != 200:
                response_text = response.text
                logger.error(f"Video service returned error: {response.status_code} - {response_text}")
                raise httpx.HTTPError(f"Video service error: {response.status_code} - {response_text}")
            
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Video synthesis job submitted successfully: {result}")
            
            # VideoService返回格式: {"code": 0, "message": "...", "data": {"job_id": "...", "task_id": "...", "status": "..."}}
            if result.get("code") == 0 and "data" in result:
                return result["data"].get("job_id", task_id)
            else:
                logger.warning(f"Video service returned non-zero code: {result}")
                return task_id
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error submitting video synthesis job: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            raise APICallException("VideoService", str(e))
        except Exception as e:
            logger.error(f"Unexpected error in video synthesis submission: {e}")
            raise APICallException("VideoService", str(e))
    
    async def get_job_status(self, job_id: str) -> dict:
        """
        获取视频合成任务状态
        
        Args:
            job_id: 任务ID (注意：这里应该是job_id而不是task_id)
            
        Returns:
            dict: 任务状态
        """
        try:
            url = f"{self.base_url}/internal/video-synthesis/jobs/{job_id}"
            
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
