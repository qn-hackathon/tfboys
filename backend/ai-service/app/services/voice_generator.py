"""
配音生成服务 - 使用七牛 AI Token API TTS 生成中文配音
"""
import logging
import httpx
import base64
import json
from io import BytesIO
from typing import Tuple
from mutagen.mp3 import MP3

from app.config import settings
from app.utils.retry import retry_on_failure
from shared.exceptions import VoiceGenerationException
from shared.enums import TTSVoice

logger = logging.getLogger(__name__)


def _get_storage_client():
    """动态获取本地存储客户端"""
    from shared.clients import get_local_storage_client
    client = get_local_storage_client()
    if client is None:
        raise RuntimeError(
            "LocalStorageClient not initialized. "
            "Please call init_local_storage_client() before using VoiceGenerator."
        )
    return client

VOICE_MAPPING = {
    TTSVoice.MALE: "zh-CN-YunxiNeural",
    TTSVoice.FEMALE: "zh-CN-XiaoxiaoNeural",
    TTSVoice.CHILD: "zh-CN-YunyangNeural"
}


class VoiceGenerator:
    """
    七牛 AI Token API TTS 配音生成服务
    
    职责:
    1. 调用七牛 AI Token API TTS 生成语音
    2. 将音频文件上传到本地存储
    3. 返回音频文件 URL 和时长
    """
    
    def __init__(self):
        self.api_key = settings.qiniu_api_key
        self.api_url = "https://openai.qiniu.com/v1/voice/tts"
    
    async def generate_voice(
        self,
        text: str,
        task_id: str,
        scene_id: str,
        voice: TTSVoice = TTSVoice.FEMALE,
        format: str = "mp3"
    ) -> Tuple[str, float]:
        """
        生成配音并上传到本地存储
        
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
            voice_type = VOICE_MAPPING.get(voice, "zh-CN-XiaoxiaoNeural")
            
            logger.info(
                f"Generating voice for task {task_id}, scene {scene_id}, "
                f"text length: {len(text)}, voice: {voice_type}"
            )
            
            audio_bytes = await self._call_tts_api(text, voice_type, format)
            
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
        voice_type: str, 
        format: str = "mp3"
    ) -> bytes:
        """
        调用七牛 AI Token API TTS
        
        Args:
            text: 文本内容
            voice_type: 音色类型
            format: 音频格式
            
        Returns:
            bytes: 音频文件字节流
            
        Raises:
            VoiceGenerationException: API 调用失败
        """
        request_body = {
            "audio": {
                "voice_type": voice_type,
                "encoding": format,
                "speed_ratio": 1.0
            },
            "request": {
                "text": text
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json=request_body,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise VoiceGenerationException(
                    f"TTS API failed: {response.status_code} - {response.text}"
                )
            
            result = response.json()
            
            data = result.get("data")
            if not data:
                raise VoiceGenerationException("No audio data in response")
            
            audio_bytes = base64.b64decode(data)
            
            return audio_bytes
    
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
        保存音频到本地存储

        Args:
            audio_bytes: 音频文件字节流
            task_id: 任务 ID
            scene_id: 场景 ID

        Returns:
            str: 音频文件本地路径
        """
        object_key = f"audio/{task_id}/{scene_id}.mp3"
        storage_client = _get_storage_client()
        local_path = await storage_client.upload_file(audio_bytes, object_key)
        return local_path


voice_generator = VoiceGenerator()
