"""
测试图像生成服务
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.image_generator import ImageGenerator
from shared.exceptions import ImageGenerationException


@pytest.mark.unit
class TestImageGenerator:
    @pytest.fixture
    def image_generator(self, mock_qiniu_image_client):
        """创建ImageGenerator实例"""
        with patch('app.services.image_generator.AsyncOpenAI', return_value=mock_qiniu_image_client):
            generator = ImageGenerator()
            return generator
    
    @pytest.mark.asyncio
    async def test_generate_scene_image_success(self, image_generator, mock_local_storage_client, mock_httpx_client):
        """测试成功生成场景图像"""
        with patch('shared.clients.local_storage_client', mock_local_storage_client), \
             patch('httpx.AsyncClient') as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = mock_httpx_client
            
            image_url = await image_generator.generate_scene_image(
                scene_description="校园樱花飘落",
                scene_id="scene_001"
            )
        
        assert image_url == "/tmp/tfboys/test_file.png"
        image_generator.client.images.generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_image_with_different_aspect_ratios(self, image_generator, mock_local_storage_client, mock_httpx_client):
        """测试不同宽高比的图像生成"""
        with patch('shared.clients.local_storage_client', mock_local_storage_client), \
             patch('httpx.AsyncClient') as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = mock_httpx_client
            
            image_url = await image_generator.generate_image(
                prompt="测试图像",
                ar="16:9"
            )
        
        assert image_url == "/tmp/tfboys/test_file.png"
        call_args = image_generator.client.images.generate.call_args
        assert call_args.kwargs["size"] == "1792x1024"
    
    def test_get_size_from_aspect_ratio(self, image_generator):
        """测试宽高比转换"""
        assert image_generator._get_size_from_aspect_ratio("1:1") == "1024x1024"
        assert image_generator._get_size_from_aspect_ratio("16:9") == "1792x1024"
        assert image_generator._get_size_from_aspect_ratio("9:16") == "1024x1792"
        assert image_generator._get_size_from_aspect_ratio("invalid") == "1024x1024"
    
    @pytest.mark.asyncio
    async def test_generate_and_upload_api_failure(self, image_generator):
        """测试API调用失败"""
        image_generator.client.images.generate = AsyncMock(side_effect=Exception("API Error"))
        
        with pytest.raises(ImageGenerationException, match="Failed to generate and upload image"):
            await image_generator._generate_and_upload(
                prompt="test",
                size="1024x1024",
                object_key="test.png"
            )
    
    @pytest.mark.asyncio
    async def test_generate_and_upload_download_failure(self, image_generator, mock_local_storage_client):
        """测试下载图像失败"""
        mock_error_response = AsyncMock()
        mock_error_response.status_code = 500
        mock_error_response.raise_for_status = AsyncMock(side_effect=Exception("Download Error"))
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_httpx = AsyncMock()
            mock_httpx.get = AsyncMock(return_value=mock_error_response)
            mock_client_class.return_value.__aenter__.return_value = mock_httpx
            
            with pytest.raises(ImageGenerationException):
                await image_generator._generate_and_upload(
                    prompt="test",
                    size="1024x1024",
                    object_key="test.png"
                )
