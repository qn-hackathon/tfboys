"""
测试视频服务客户端
"""
import pytest
from unittest.mock import patch, AsyncMock
from app.services.video_client import VideoClient
from shared.models.scene import Scene
from shared.exceptions import APICallException


@pytest.mark.unit
class TestVideoClient:
    @pytest.fixture
    def video_client(self):
        """创建VideoClient实例"""
        return VideoClient(base_url="http://test-video-service:8003", timeout=30)
    
    @pytest.fixture
    def sample_scenes(self):
        """示例场景列表"""
        return [
            Scene(
                scene_id="scene_001",
                scene_index=0,
                description="测试场景1",
                narration="测试旁白1",
                characters=[],
                image_url="/tmp/scene_001.png",
                audio_url="/tmp/audio_001.mp3",
                duration=5.0
            ),
            Scene(
                scene_id="scene_002",
                scene_index=1,
                description="测试场景2",
                narration="测试旁白2",
                characters=[],
                image_url="/tmp/scene_002.png",
                audio_url="/tmp/audio_002.mp3",
                duration=6.0
            )
        ]
    
    @pytest.mark.asyncio
    async def test_submit_video_synthesis_job_success(self, video_client, sample_scenes):
        """测试成功提交视频合成任务"""
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"task_id": "test_task_001"})
        mock_response.raise_for_status = AsyncMock()
        
        video_client.client.post = AsyncMock(return_value=mock_response)
        
        task_id = await video_client.submit_video_synthesis_job("test_task_001", sample_scenes)
        
        assert task_id == "test_task_001"
        video_client.client.post.assert_called_once()
        call_args = video_client.client.post.call_args
        assert "http://test-video-service:8003/internal/synthesize" in call_args[0]
    
    @pytest.mark.asyncio
    async def test_submit_video_synthesis_job_http_error(self, video_client, sample_scenes):
        """测试HTTP错误"""
        import httpx
        video_client.client.post = AsyncMock(side_effect=httpx.HTTPError("Connection Error"))
        
        with pytest.raises(APICallException):
            await video_client.submit_video_synthesis_job("test_task", sample_scenes)
    
    @pytest.mark.asyncio
    async def test_get_job_status_success(self, video_client):
        """测试成功获取任务状态"""
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            "task_id": "test_task",
            "status": "completed",
            "video_url": "/tmp/video.mp4"
        })
        mock_response.raise_for_status = AsyncMock()
        
        video_client.client.get = AsyncMock(return_value=mock_response)
        
        status = await video_client.get_job_status("test_task")
        
        assert status["status"] == "completed"
        assert status["video_url"] == "/tmp/video.mp4"
    
    @pytest.mark.asyncio
    async def test_get_job_status_error(self, video_client):
        """测试获取状态失败"""
        import httpx
        video_client.client.get = AsyncMock(side_effect=httpx.HTTPError("Not Found"))
        
        with pytest.raises(APICallException):
            await video_client.get_job_status("test_task")
    
    @pytest.mark.asyncio
    async def test_close(self, video_client):
        """测试关闭客户端"""
        video_client.client.aclose = AsyncMock()
        
        await video_client.close()
        
        video_client.client.aclose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """测试上下文管理器"""
        async with VideoClient("http://test:8003") as client:
            assert client is not None
            client.client.aclose = AsyncMock()
