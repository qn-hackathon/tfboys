"""
图像生成服务 - 使用 OpenAI DALL-E 3 API 生成动漫风格图像
"""
import httpx
import logging
from typing import Optional
from openai import AsyncOpenAI
from app.config import settings
from shared.clients import oss_client

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "dall-e-3"
        self.quality = "standard"
    
    async def generate_character_image(
        self,
        character_name: str,
        character_description: str,
    ) -> str:
        """
        生成角色设定图
        
        Args:
            character_name: 角色名称
            character_description: 角色外貌描述
        
        Returns:
            str: 上传到 OSS 后的图像 URL
        """
        prompt = (
            f"Anime style character design sheet for {character_name}. "
            f"{character_description}. "
            f"Full body character design, white background, character sheet style, "
            f"high quality anime illustration, detailed character design."
        )
        
        logger.info(f"Generating character image for '{character_name}'")
        
        image_url = await self._generate_and_upload(
            prompt=prompt,
            size="1024x1024",
            object_key=f"characters/{character_name.replace(' ', '_')}.png"
        )
        
        logger.info(f"Character image generated for '{character_name}': {image_url}")
        return image_url
    
    async def generate_scene_image(
        self,
        scene_description: str,
        scene_id: str,
        character_context: Optional[str] = None
    ) -> str:
        """
        生成场景图像
        
        注意: DALL-E 3 不支持 --cref 参数,但我们可以在 prompt 中描述角色特征
        以保持一定的角色一致性
        
        Args:
            scene_description: 场景描述
            scene_id: 场景ID (用于生成文件名)
            character_context: 角色上下文描述 (可选,用于保持角色一致性)
        
        Returns:
            str: 上传到 OSS 后的图像 URL
        """
        prompt = f"Anime style scene. {scene_description}."
        
        if character_context:
            prompt += f" Characters in scene: {character_context}."
        
        prompt += " Cinematic composition, high quality anime illustration, detailed background."
        
        logger.info(f"Generating scene image for scene_id: {scene_id}")
        
        image_url = await self._generate_and_upload(
            prompt=prompt,
            size="1792x1024",
            object_key=f"scenes/{scene_id}.png"
        )
        
        logger.info(f"Scene image generated for {scene_id}: {image_url}")
        return image_url
    
    async def generate_image(
        self,
        prompt: str,
        character_ref_url: Optional[str] = None,
        ar: str = "16:9"
    ) -> str:
        """
        通用图像生成接口 (兼容旧的 API)
        
        Args:
            prompt: 图像描述
            character_ref_url: 角色参考图 URL (注意: DALL-E 3 不支持引用图像)
            ar: 宽高比 (支持: "1:1", "16:9", "9:16")
        
        Returns:
            str: 上传到 OSS 后的图像 URL
        """
        size = self._get_size_from_aspect_ratio(ar)
        
        if character_ref_url:
            logger.warning(
                "DALL-E 3 does not support character reference images. "
                "Character consistency will be maintained through detailed prompts only."
            )
        
        full_prompt = f"{prompt}. High quality anime illustration."
        
        logger.info(f"Generating image with prompt: {full_prompt[:100]}...")
        
        image_url = await self._generate_and_upload(
            prompt=full_prompt,
            size=size,
            object_key=f"generated/{hash(full_prompt) % 10000000}.png"
        )
        
        return image_url
    
    async def _generate_and_upload(
        self,
        prompt: str,
        size: str,
        object_key: str
    ) -> str:
        """
        生成图像并上传到 OSS
        
        Args:
            prompt: 生成提示词
            size: 图像尺寸 ("1024x1024", "1792x1024", "1024x1792")
            object_key: OSS 对象键
        
        Returns:
            str: OSS 中的图像 URL
        """
        try:
            response = await self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=self.quality,
                n=1,
            )
            
            dalle_image_url = response.data[0].url
            logger.info(f"DALL-E 3 image generated: {dalle_image_url}")
            
            async with httpx.AsyncClient() as client:
                image_response = await client.get(dalle_image_url)
                image_response.raise_for_status()
                image_bytes = image_response.content
            
            oss_url = await oss_client.upload_file(image_bytes, object_key)
            
            logger.info(f"Image uploaded to OSS: {oss_url}")
            return oss_url
            
        except Exception as e:
            logger.error(f"Failed to generate and upload image: {str(e)}", exc_info=True)
            raise
    
    def _get_size_from_aspect_ratio(self, ar: str) -> str:
        """
        根据宽高比获取 DALL-E 3 支持的尺寸
        
        Args:
            ar: 宽高比 ("1:1", "16:9", "9:16")
        
        Returns:
            str: DALL-E 3 尺寸 ("1024x1024", "1792x1024", "1024x1792")
        """
        size_map = {
            "1:1": "1024x1024",
            "16:9": "1792x1024",
            "9:16": "1024x1792",
        }
        return size_map.get(ar, "1024x1024")


image_generator = ImageGenerator()
