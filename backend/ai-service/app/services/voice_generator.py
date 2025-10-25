"""
配音生成服务 - 使用阿里云TTS生成中文配音
"""
import asyncio
import logging
import json
import uuid
from typing import Optional
import httpx
from app.config import settings
from shared.exceptions import VoiceGenerationException
from shared.clients import oss_client, init_oss_client

logger = logging.getLogger(__name__)


class VoiceGenerator:
    def __init__(self):
        self.access_key_id = settings.aliyun_tts_access_key_id
        self.access_key_secret = settings.aliyun_tts_access_key_secret
        self.app_key = settings.aliyun_tts_app_key
        
        self.voice_mapping = {
            "zhiyan": "zhiyan",
            "zhixiaobai": "zhixiaobai",
            "zhimiao": "zhimiao",
            "xiaoyun": "xiaoyun",
            "xiaogang": "xiaogang"
        }
        
        if not oss_client:
            init_oss_client(
                access_key_id=settings.oss_access_key_id,
                access_key_secret=settings.oss_access_key_secret,
                endpoint=settings.oss_endpoint,
                bucket_name=settings.oss_bucket_name
            )
    
    async def generate_voice(self, text: str, voice: str = "zhiyan") -> str:
        """
        生成配音
        
        Args:
            text: 文字内容
            voice: 音色 (支持: zhiyan, zhixiaobai, zhimiao, xiaoyun, xiaogang)
        
        Returns:
            音频文件URL (OSS上传后的URL)
            
        Raises:
            VoiceGenerationException: 配音生成失败
        """
        try:
            if not text or not text.strip():
                raise VoiceGenerationException("Text content is empty")
            
            voice_name = self.voice_mapping.get(voice, "zhiyan")
            logger.info(f"Generating voice for text (length: {len(text)}) with voice: {voice_name}")
            
            audio_data = await self._call_aliyun_tts(text, voice_name)
            
            audio_filename = f"audio/{uuid.uuid4()}.mp3"
            audio_url = await oss_client.upload_file(audio_data, audio_filename)
            
            logger.info(f"Voice generated and uploaded: {audio_url}")
            return audio_url
            
        except Exception as e:
            logger.error(f"Failed to generate voice: {e}", exc_info=True)
            raise VoiceGenerationException(str(e))
    
    async def _call_aliyun_tts(self, text: str, voice: str) -> bytes:
        """
        调用阿里云TTS API
        
        Args:
            text: 文字内容
            voice: 音色
            
        Returns:
            bytes: 音频数据 (MP3格式)
            
        Raises:
            VoiceGenerationException: API调用失败
        """
        try:
            url = "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts"
            
            params = {
                "appkey": self.app_key,
                "token": await self._get_token(),
                "text": text,
                "format": "mp3",
                "sample_rate": 16000,
                "voice": voice,
                "volume": 50,
                "speech_rate": 0,
                "pitch_rate": 0
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, data=params)
                response.raise_for_status()
                
                content_type = response.headers.get("content-type", "")
                if "audio" in content_type:
                    return response.content
                else:
                    error_msg = response.text
                    logger.error(f"Aliyun TTS API error: {error_msg}")
                    raise VoiceGenerationException(f"API returned error: {error_msg}")
                    
        except httpx.HTTPError as e:
            logger.error(f"Aliyun TTS HTTP error: {e}")
            raise VoiceGenerationException(f"HTTP error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error calling Aliyun TTS: {e}", exc_info=True)
            raise VoiceGenerationException(str(e))
    
    async def _get_token(self) -> str:
        """
        获取阿里云TTS访问令牌
        
        Returns:
            str: Access Token
            
        Raises:
            VoiceGenerationException: 获取Token失败
        """
        try:
            url = "https://nls-meta.cn-shanghai.aliyuncs.com/token"
            
            params = {
                "AccessKeyId": self.access_key_id,
                "Action": "CreateToken"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                result = response.json()
                
                if "Token" in result and "Id" in result["Token"]:
                    token = result["Token"]["Id"]
                    logger.info("Aliyun TTS token obtained successfully")
                    return token
                else:
                    error_msg = result.get("Message", "Unknown error")
                    raise VoiceGenerationException(f"Failed to get token: {error_msg}")
                    
        except httpx.HTTPError as e:
            logger.error(f"Failed to get Aliyun TTS token: {e}")
            raise VoiceGenerationException(f"Token request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error getting token: {e}", exc_info=True)
            raise VoiceGenerationException(str(e))


voice_generator = VoiceGenerator()
