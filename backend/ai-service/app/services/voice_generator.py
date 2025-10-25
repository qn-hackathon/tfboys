"""
配音生成服务 - 使用阿里云TTS生成中文配音
"""
import logging
import httpx
from io import BytesIO
from typing import Tuple
from mutagen.mp3 import MP3

from app.config import settings
from app.utils.retry import retry_on_failure
from shared.clients.oss_client import init_oss_client, oss_client
from shared.exceptions import VoiceGenerationException
from shared.enums import TTSVoice

logger = logging.getLogger(__name__)

VOICE_MAPPING = {
    TTSVoice.MALE: "zhiyan",
    TTSVoice.FEMALE: "aitong",
    TTSVoice.CHILD: "aixia"
}


class VoiceGenerator:
    """
    阿里云 TTS 配音生成服务
    
    职责:
    1. 调用阿里云 NLS TTS API 生成语音
    2. 将音频文件上传到 OSS
    3. 返回音频文件 URL 和时长
    """
    
    def __init__(self):
        self.access_key_id = settings.aliyun_tts_access_key_id
        self.access_key_secret = settings.aliyun_tts_access_key_secret
        self.app_key = settings.aliyun_tts_app_key
        self.api_url = "https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts"
        
        if not oss_client:
            init_oss_client(
                access_key_id=settings.oss_access_key_id,
                access_key_secret=settings.oss_access_key_secret,
                endpoint=settings.oss_endpoint,
                bucket_name=settings.oss_bucket_name
            )
    
    async def generate_voice(
        self,
        text: str,
        task_id: str,
        scene_id: str,
        voice: TTSVoice = TTSVoice.FEMALE,
        format: str = "mp3"
    ) -> Tuple[str, float]:
        """
        生成配音并上传到 OSS
        
        Args:
            text: 旁白文字
            task_id: 任务 ID
            scene_id: 场景 ID
            voice: 音色类型
            format: 音频格式
            
        Returns:
            tuple[str, float]: (音频 URL, 音频时长)
            
        Raises:
            VoiceGenerationException: 配音生成失败
        """
        try:
            voice_code = VOICE_MAPPING.get(voice, "aitong")
            
            logger.info(
                f"Generating voice for task {task_id}, scene {scene_id}, "
                f"text length: {len(text)}, voice: {voice_code}"
            )
            
            audio_bytes = await self._call_tts_api(text, voice_code, format)
            
            duration = self._get_audio_duration(audio_bytes)
            
            audio_url = await self._upload_to_oss(audio_bytes, task_id, scene_id)
            
            logger.info(
                f"Voice generated successfully: {audio_url}, duration: {duration}s"
            )
            
            return audio_url, duration
            
        except Exception as e:
            logger.error(f"Failed to generate voice: {e}", exc_info=True)
            raise VoiceGenerationException(str(e))
    
    @retry_on_failure(max_retries=3, delay=2.0, backoff=2.0)
    async def _call_tts_api(
        self, 
        text: str, 
        voice: str, 
        format: str = "mp3"
    ) -> bytes:
        """
        调用阿里云 TTS API
        
        Args:
            text: 文本内容
            voice: 音色代码
            format: 音频格式
            
        Returns:
            bytes: 音频文件字节流
            
        Raises:
            VoiceGenerationException: API 调用失败
        """
        params = {
            "appkey": self.app_key,
            "text": text,
            "voice": voice,
            "format": format,
            "sample_rate": 16000,
            "volume": 50
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json=params,
                headers=headers,
                auth=(self.access_key_id, self.access_key_secret),
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise VoiceGenerationException(
                    f"TTS API failed: {response.status_code} - {response.text}"
                )
            
            return response.content
    
    def _get_audio_duration(self, audio_bytes: bytes) -> float:
        """
        获取音频时长
        
        Args:
            audio_bytes: 音频文件字节流
            
        Returns:
            float: 时长(秒)
        """
        try:
            audio = MP3(BytesIO(audio_bytes))
            return audio.info.length
        except Exception as e:
            logger.warning(f"Failed to get audio duration: {e}, using default 5.0s")
            return 5.0
    
    async def _upload_to_oss(
        self, 
        audio_bytes: bytes, 
        task_id: str, 
        scene_id: str
    ) -> str:
        """
        上传音频到 OSS
        
        Args:
            audio_bytes: 音频文件字节流
            task_id: 任务 ID
            scene_id: 场景 ID
            
        Returns:
            str: 音频文件 URL
        """
        object_key = f"audio/{task_id}/{scene_id}.mp3"
        url = await oss_client.upload_file(audio_bytes, object_key)
        return url


voice_generator = VoiceGenerator()
