"""
配音生成服务 - 使用七牛云TTS生成中文配音
"""
import asyncio
import logging
import json
import uuid
import hmac
import hashlib
import base64
from typing import Optional
from urllib.parse import urlparse
import httpx
from app.config import settings
from shared.exceptions import VoiceGenerationException
from shared.clients import oss_client, init_oss_client

logger = logging.getLogger(__name__)


class VoiceGenerator:
    def __init__(self):
        self.access_key = settings.qiniu_access_key
        self.secret_key = settings.qiniu_secret_key
        self.tts_url = "https://ap-gate-z0.qiniuapi.com/voice/v2/tts"
        
        self.voice_mapping = {
            "mature_female": 7,
            "shaanxi_male": 8,
            "northeast_male": 9,
            "mature_male": 10,
            "boy_male": 11,
            "narrator_male": 12,
            "news_male": 13,
            "adolescent_female": 14
        }
        
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
        voice: str = "mature_female",
        speed: float = 1.0,
        volume: float = 1.0
    ) -> str:
        """
        生成配音
        
        Args:
            text: 文字内容 (1-200字符)
            voice: 音色 (支持: mature_female, shaanxi_male, northeast_male, 
                   mature_male, boy_male, narrator_male, news_male, adolescent_female)
            speed: 语速 (0.75-1.25)
            volume: 音量 (0.75-1.25)
        
        Returns:
            音频文件URL (OSS上传后的URL)
            
        Raises:
            VoiceGenerationException: 配音生成失败
        """
        try:
            if not text or not text.strip():
                raise VoiceGenerationException("Text content is empty")
            
            if len(text) > 200:
                raise VoiceGenerationException("Text exceeds 200 characters limit")
            
            spkid = self.voice_mapping.get(voice, 7)
            logger.info(f"Generating voice for text (length: {len(text)}) with voice ID: {spkid}")
            
            audio_url = await self._call_qiniu_tts(
                text=text, 
                spkid=spkid,
                speed=speed,
                volume=volume
            )
            
            audio_data = await self._download_audio(audio_url)
            
            audio_filename = f"audio/{uuid.uuid4()}.mp3"
            oss_url = await oss_client.upload_file(audio_data, audio_filename)
            
            logger.info(f"Voice generated and uploaded: {oss_url}")
            return oss_url
            
        except Exception as e:
            logger.error(f"Failed to generate voice: {e}", exc_info=True)
            raise VoiceGenerationException(str(e))
    
    async def _call_qiniu_tts(
        self, 
        text: str, 
        spkid: int,
        speed: float,
        volume: float
    ) -> str:
        """
        调用七牛云TTS API
        
        Args:
            text: 文字内容
            spkid: 音色ID (7-14)
            speed: 语速 (0.75-1.25)
            volume: 音量 (0.75-1.25)
            
        Returns:
            str: 音频文件下载URL
            
        Raises:
            VoiceGenerationException: API调用失败
        """
        try:
            payload = {
                "content": text,
                "spkid": spkid,
                "audioType": 3,
                "volume": max(0.75, min(1.25, volume)),
                "speed": max(0.75, min(1.25, speed))
            }
            
            body = json.dumps(payload).encode('utf-8')
            auth_header = self._generate_qiniu_auth(
                url=self.tts_url,
                method="POST",
                body=body,
                content_type="application/json"
            )
            
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.tts_url, 
                    content=body,
                    headers=headers
                )
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("code") == 0:
                    audio_url = result.get("result", {}).get("audioUrl")
                    if not audio_url:
                        raise VoiceGenerationException("No audioUrl in response")
                    logger.info(f"Qiniu TTS API success: {audio_url}")
                    return audio_url
                else:
                    error_msg = result.get("msg", "Unknown error")
                    raise VoiceGenerationException(f"API returned error: {error_msg}")
                    
        except httpx.HTTPError as e:
            logger.error(f"Qiniu TTS HTTP error: {e}")
            raise VoiceGenerationException(f"HTTP error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error calling Qiniu TTS: {e}", exc_info=True)
            raise VoiceGenerationException(str(e))
    
    def _generate_qiniu_auth(
        self, 
        url: str, 
        method: str = "POST",
        body: bytes = b"",
        content_type: str = "application/json"
    ) -> str:
        """
        生成七牛云认证签名
        
        Args:
            url: API URL
            method: HTTP方法
            body: 请求体
            content_type: Content-Type
            
        Returns:
            str: Authorization header值
        """
        parsed_url = urlparse(url)
        path = parsed_url.path
        if parsed_url.query:
            path += f"?{parsed_url.query}"
        
        data_to_sign = f"{method} {path}\nHost: {parsed_url.netloc}\n"
        
        if content_type:
            data_to_sign += f"Content-Type: {content_type}\n"
        
        data_to_sign += "\n"
        
        if body and content_type == "application/json":
            data_to_sign += body.decode('utf-8')
        
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
        
        encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8')
        
        return f"Qiniu {self.access_key}:{encoded_signature}"
    
    async def _download_audio(self, audio_url: str) -> bytes:
        """
        下载音频文件
        
        Args:
            audio_url: 音频文件URL
            
        Returns:
            bytes: 音频数据
            
        Raises:
            VoiceGenerationException: 下载失败
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(audio_url)
                response.raise_for_status()
                return response.content
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to download audio: {e}")
            raise VoiceGenerationException(f"Audio download failed: {str(e)}")


voice_generator = VoiceGenerator()
