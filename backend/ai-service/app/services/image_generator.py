"""
图像生成服务 - 使用七牛文生图 API 生成动漫风格图像
"""
import httpx
import logging
import base64
from typing import Optional
from openai import AsyncOpenAI
from app.config import settings
from shared.exceptions import ImageGenerationException
from app.utils.retry import retry_on_failure

logger = logging.getLogger(__name__)


def _get_storage_client():
    """动态获取本地存储客户端"""
    from shared.clients import get_local_storage_client
    client = get_local_storage_client()
    if client is None:
        raise RuntimeError(
            "LocalStorageClient not initialized. "
            "Please call init_local_storage_client() before using ImageGenerator."
        )
    return client


class ImageGenerator:
    """图像生成器 - 基于七牛 AI Token API"""

    def __init__(self):
        # 七牛 AI Token API 使用 OpenAI SDK 兼容接口
        self.client = AsyncOpenAI(
            base_url="https://openai.qiniu.com/v1",
            api_key=settings.qiniu_api_key
        )
        # 使用七牛支持的图像生成模型
        self.model = "gemini-2.5-flash-image"
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
            str: 上传到本地存储后的图像路径
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

        Args:
            scene_description: 场景描述
            scene_id: 场景ID (用于生成文件名)
            character_context: 角色上下文描述 (可选,用于保持角色一致性)

        Returns:
            str: 上传到本地存储后的图像路径
        """
        prompt = f"Anime style scene. {scene_description}."

        if character_context:
            prompt += f" Characters in scene: {character_context}."

        prompt += " Cinematic composition, high quality anime illustration, detailed background."

        logger.info(f"Generating scene image for scene_id: {scene_id}")

        image_url = await self._generate_and_upload(
            prompt=prompt,
            size="1792x1024",  # 16:9 横屏比例
            object_key=f"scenes/{scene_id}.png"
        )

        logger.info(f"Scene image generated for {scene_id}: {image_url}")
        return image_url

    @retry_on_failure(max_retries=3, delay=5.0, backoff=2.0)
    async def generate_image(
        self,
        prompt: str,
        character_ref_url: Optional[str] = None,
        ar: str = "16:9"
    ) -> str:
        """
        通用图像生成接口

        Args:
            prompt: 图像描述
            character_ref_url: 角色参考图 URL (注意: 当前不支持引用图像)
            ar: 宽高比 (支持: "1:1", "16:9", "9:16")

        Returns:
            str: 上传到本地存储后的图像路径
        """
        size = self._get_size_from_aspect_ratio(ar)

        if character_ref_url:
            logger.warning(
                "Qiniu text-to-image API does not support character reference images. "
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

    @retry_on_failure(max_retries=3, delay=2.0, backoff=2.0)
    async def _generate_and_upload(
        self,
        prompt: str,
        size: str,
        object_key: str
    ) -> str:
        """
        生成图像并上传到本地存储

        Args:
            prompt: 生成提示词
            size: 图像尺寸 (如: "1024x1024", "1792x1024", "1024x1792")
            object_key: 存储对象键

        Returns:
            str: 本地存储中的图像路径

        Raises:
            ImageGenerationException: 图像生成失败
        """
        try:
            # 调用七牛文生图 API
            response = await self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                n=1,
            )

            # 七牛 API 返回 base64 编码的图片数据
            if hasattr(response.data[0], 'b64_json'):
                # Base64 格式
                image_base64 = response.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)
                logger.info(f"Qiniu image generated (base64 format)")
            elif hasattr(response.data[0], 'url'):
                # URL 格式 (备用)
                image_url = response.data[0].url
                logger.info(f"Qiniu image generated: {image_url}")

                # 下载图片
                async with httpx.AsyncClient() as client:
                    image_response = await client.get(image_url)
                    image_response.raise_for_status()
                    image_bytes = image_response.content
            else:
                raise ImageGenerationException("Invalid response format from Qiniu API")

            # 上传到本地存储
            storage_client = _get_storage_client()
            local_path = await storage_client.upload_file(image_bytes, object_key)

            logger.info(f"Image saved to local storage: {local_path}")
            return local_path

        except Exception as e:
            logger.error(f"Failed to generate and upload image: {str(e)}", exc_info=True)
            raise ImageGenerationException(f"Failed to generate and upload image: {str(e)}")

    def _get_size_from_aspect_ratio(self, ar: str) -> str:
        """
        根据宽高比获取七牛 API 支持的尺寸

        支持的尺寸:
        - 正方形: 1024x1024
        - 横屏: 1536x1024, 1792x1024, 1344x768
        - 竖屏: 1024x1536, 1024x1792, 768x1344

        Args:
            ar: 宽高比 ("1:1", "16:9", "9:16", "4:3", "3:4")

        Returns:
            str: 图像尺寸
        """
        size_map = {
            "1:1": "1024x1024",
            "16:9": "1792x1024",
            "9:16": "1024x1792",
            "4:3": "1344x768",
            "3:4": "768x1344",
        }
        size = size_map.get(ar, "1024x1024")
        if ar not in size_map:
            logger.warning(f"Unsupported aspect ratio '{ar}', using default 1024x1024")
        return size

    async def close(self):
        """关闭客户端"""
        await self.client.close()


# 全局单例
image_generator = ImageGenerator()
