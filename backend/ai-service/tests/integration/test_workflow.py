"""
集成测试 - 完整工作流程
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.workers.tasks import _process_novel_task_async
from shared.enums import TaskStatus


@pytest.mark.integration
class TestNovelProcessingWorkflow:
    @pytest.fixture
    def mock_all_clients(self, mock_redis_client, mock_local_storage_client, mock_anthropic_client, mock_openai_client):
        """Mock所有外部客户端"""
        return {
            'redis': mock_redis_client,
            'storage': mock_local_storage_client,
            'anthropic': mock_anthropic_client,
            'openai': mock_openai_client
        }
    
    @pytest.mark.asyncio
    async def test_complete_workflow_success(
        self, mock_all_clients, sample_novel_text, sample_scenes_data
    ):
        """测试完整工作流程成功"""
        mock_redis = mock_all_clients['redis']
        mock_storage = mock_all_clients['storage']
        mock_anthropic = mock_all_clients['anthropic']
        mock_openai = mock_all_clients['openai']
        
        mock_anthropic_response = MagicMock()
        mock_anthropic_response.content = [MagicMock(text='{"scenes": ' + str(sample_scenes_data).replace("'", '"') + '}')]
        mock_anthropic.messages.create = MagicMock(return_value=mock_anthropic_response)
        
        mock_tts_response = AsyncMock()
        mock_tts_response.status_code = 200
        mock_tts_response.json = AsyncMock(return_value={
            "code": "0",
            "result": {"audioUrl": "https://example.com/audio.mp3"}
        })
        
        mock_audio_download = AsyncMock()
        mock_audio_download.status_code = 200
        mock_audio_download.content = b"audio_data"
        
        mock_httpx = AsyncMock()
        mock_httpx.get = AsyncMock(return_value=AsyncMock(
            status_code=200,
            content=b"image_data",
            raise_for_status=AsyncMock()
        ))
        mock_httpx.post = AsyncMock(return_value=mock_tts_response)
        
        mock_video_response = AsyncMock()
        mock_video_response.json = AsyncMock(return_value={"task_id": "test_task"})
        mock_video_response.raise_for_status = AsyncMock()
        
        with patch('shared.clients.redis_client', mock_redis), \
             patch('shared.clients.local_storage_client', mock_storage), \
             patch('app.services.text_analyzer.Anthropic', return_value=mock_anthropic), \
             patch('app.services.image_generator.AsyncOpenAI', return_value=mock_openai), \
             patch('httpx.AsyncClient') as mock_client_class, \
             patch('asyncio.to_thread', return_value=mock_anthropic_response), \
             patch('app.services.voice_generator.MP3') as mock_mp3:
            
            mock_client_class.return_value.__aenter__.return_value = mock_httpx
            mock_httpx_for_tts = AsyncMock()
            mock_httpx_for_tts.post = AsyncMock(return_value=mock_tts_response)
            mock_httpx_for_tts.get = AsyncMock(return_value=mock_audio_download)
            
            mock_audio_info = MagicMock()
            mock_audio_info.info.length = 5.0
            mock_mp3.return_value = mock_audio_info
            
            mock_video_client = AsyncMock()
            mock_video_client.submit_video_synthesis_job = AsyncMock(return_value="video_job_123")
            
            with patch('app.services.video_client.video_client', mock_video_client):
                result = await _process_novel_task_async("test_task_001", sample_novel_text)
        
        assert result["status"] == "success"
        assert result["task_id"] == "test_task_001"
        assert result["total_scenes"] == 2
        
        mock_redis.update_task_status.assert_any_call("test_task_001", TaskStatus.ANALYZING.value)
        mock_redis.update_task_status.assert_any_call("test_task_001", TaskStatus.GENERATING_IMAGES.value)
    
    @pytest.mark.asyncio
    async def test_workflow_text_analysis_failure(
        self, mock_all_clients, sample_novel_text
    ):
        """测试文本分析失败"""
        mock_redis = mock_all_clients['redis']
        
        with patch('shared.clients.redis_client', mock_redis), \
             patch('app.services.text_analyzer.text_analyzer.analyze_novel', side_effect=Exception("Analysis Error")):
            
            with pytest.raises(Exception, match="Analysis Error"):
                await _process_novel_task_async("test_task", sample_novel_text)
            
            mock_redis.update_task_status.assert_any_call(
                "test_task",
                TaskStatus.FAILED.value,
                error="Analysis Error"
            )
    
    @pytest.mark.asyncio
    async def test_workflow_empty_scenes(self, mock_all_clients, sample_novel_text):
        """测试空场景列表"""
        mock_redis = mock_all_clients['redis']
        
        with patch('shared.clients.redis_client', mock_redis), \
             patch('app.services.text_analyzer.text_analyzer.analyze_novel', return_value=[]):
            
            with pytest.raises(ValueError, match="No scenes extracted"):
                await _process_novel_task_async("test_task", sample_novel_text)
    
    @pytest.mark.asyncio
    async def test_workflow_video_submission_failure(
        self, mock_all_clients, sample_novel_text, sample_scenes_data
    ):
        """测试视频提交失败"""
        mock_redis = mock_all_clients['redis']
        mock_storage = mock_all_clients['storage']
        mock_anthropic = mock_all_clients['anthropic']
        mock_openai = mock_all_clients['openai']
        
        mock_anthropic_response = MagicMock()
        mock_anthropic_response.content = [MagicMock(text='{"scenes": ' + str(sample_scenes_data).replace("'", '"') + '}')]
        
        with patch('shared.clients.redis_client', mock_redis), \
             patch('shared.clients.local_storage_client', mock_storage), \
             patch('app.services.text_analyzer.Anthropic', return_value=mock_anthropic), \
             patch('app.services.image_generator.AsyncOpenAI', return_value=mock_openai), \
             patch('asyncio.to_thread', return_value=mock_anthropic_response), \
             patch('httpx.AsyncClient') as mock_client_class, \
             patch('app.services.voice_generator.MP3'):
            
            mock_httpx = AsyncMock()
            mock_httpx.get = AsyncMock(return_value=AsyncMock(
                status_code=200,
                content=b"data",
                raise_for_status=AsyncMock()
            ))
            mock_httpx.post = AsyncMock(return_value=AsyncMock(
                status_code=200,
                json=AsyncMock(return_value={"code": "0", "result": {"audioUrl": "http://test.mp3"}})
            ))
            mock_client_class.return_value.__aenter__.return_value = mock_httpx
            
            mock_video_client = AsyncMock()
            mock_video_client.submit_video_synthesis_job = AsyncMock(
                side_effect=Exception("Video Service Error")
            )
            
            with patch('app.services.video_client.video_client', mock_video_client):
                with pytest.raises(Exception, match="Video Service Error"):
                    await _process_novel_task_async("test_task", sample_novel_text)
