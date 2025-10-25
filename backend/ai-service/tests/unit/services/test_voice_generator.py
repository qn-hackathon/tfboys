"""
测试配音生成服务
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.voice_generator import VoiceGenerator, VOICE_MAPPING
from shared.enums import TTSVoice
from shared.exceptions import VoiceGenerationException


@pytest.mark.unit
class TestVoiceGenerator:
    @pytest.fixture
    def voice_generator(self):
        """创建VoiceGenerator实例"""
        with patch('app.services.voice_generator.settings') as mock_settings:
            mock_settings.qiniu_api_key = "test_api_key"
            generator = VoiceGenerator()
            return generator
    
    @pytest.mark.asyncio
    async def test_generate_voice_success(self, voice_generator, mock_local_storage_client):
        """测试成功生成配音"""
        fake_audio_bytes = b"fake_mp3_data" * 1000
        
        with patch.object(voice_generator, '_call_tts_api', return_value=fake_audio_bytes), \
             patch.object(voice_generator, '_get_audio_duration', return_value=5.5), \
             patch.object(voice_generator, '_upload_to_oss', return_value="/tmp/tfboys/audio/test.mp3"):
            
            audio_url, duration = await voice_generator.generate_voice(
                text="测试文本",
                task_id="test_task",
                scene_id="scene_001",
                voice=TTSVoice.FEMALE
            )
        
        assert audio_url == "/tmp/tfboys/audio/test.mp3"
        assert duration == 5.5
    
    @pytest.mark.asyncio
    async def test_generate_voice_different_voices(self, voice_generator):
        """测试不同音色"""
        with patch.object(voice_generator, '_call_tts_api', return_value=b"fake_audio"), \
             patch.object(voice_generator, '_get_audio_duration', return_value=5.0), \
             patch.object(voice_generator, '_upload_to_oss', return_value="/tmp/audio.mp3"):
            
            await voice_generator.generate_voice(
                text="测试",
                task_id="task",
                scene_id="scene",
                voice=TTSVoice.MALE
            )
            
            call_args = voice_generator._call_tts_api.call_args
            assert call_args[0][1] == VOICE_MAPPING[TTSVoice.MALE]
    
    @pytest.mark.asyncio
    async def test_generate_voice_api_failure(self, voice_generator):
        """测试API调用失败"""
        with patch.object(voice_generator, '_call_tts_api', side_effect=Exception("API Error")):
            with pytest.raises(VoiceGenerationException):
                await voice_generator.generate_voice(
                    text="测试",
                    task_id="task",
                    scene_id="scene"
                )
    
    @pytest.mark.asyncio
    async def test_call_tts_api_success(self, voice_generator):
        """测试TTS API调用成功"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value={
            "code": "0",
            "result": {"audioUrl": "https://example.com/audio.mp3"}
        })
        
        mock_audio_response = AsyncMock()
        mock_audio_response.status_code = 200
        mock_audio_response.content = b"audio_data"
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.get = AsyncMock(return_value=mock_audio_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            audio_bytes = await voice_generator._call_tts_api("测试文本", 7, "mp3")
        
        assert audio_bytes == b"audio_data"
    
    @pytest.mark.asyncio
    async def test_call_tts_api_error_response(self, voice_generator):
        """测试TTS API返回错误"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = AsyncMock(return_value={
            "code": "1",
            "msg": "API Error"
        })
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            with pytest.raises(VoiceGenerationException, match="TTS API error"):
                await voice_generator._call_tts_api("测试", 7, "mp3")
    
    def test_get_audio_duration_success(self, voice_generator):
        """测试获取音频时长成功"""
        fake_mp3_bytes = b"ID3" + b"\x00" * 100
        
        with patch('app.services.voice_generator.MP3') as mock_mp3:
            mock_audio = MagicMock()
            mock_audio.info.length = 10.5
            mock_mp3.return_value = mock_audio
            
            duration = voice_generator._get_audio_duration(fake_mp3_bytes)
        
        assert duration == 10.5
    
    def test_get_audio_duration_failure(self, voice_generator):
        """测试获取音频时长失败时使用默认值"""
        with patch('app.services.voice_generator.MP3', side_effect=Exception("Parse Error")):
            duration = voice_generator._get_audio_duration(b"invalid")
        
        assert duration == 5.0
    
    @pytest.mark.asyncio
    async def test_upload_to_oss(self, voice_generator, mock_local_storage_client):
        """测试上传到OSS"""
        with patch('shared.clients.local_storage_client', mock_local_storage_client):
            audio_url = await voice_generator._upload_to_oss(
                b"audio_bytes",
                "test_task",
                "scene_001"
            )
        
        assert audio_url == "/tmp/tfboys/test_file.png"
        mock_local_storage_client.upload_file.assert_called_once()
