"""
pytest配置和共享fixtures
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, List


@pytest.fixture
def mock_redis_client():
    """Mock Redis客户端"""
    mock_client = AsyncMock()
    mock_client.get_task = AsyncMock(return_value={
        "task_id": "test_task_001",
        "status": "pending",
        "created_at": "2024-10-25T00:00:00Z"
    })
    mock_client.save_task = AsyncMock()
    mock_client.update_task_status = AsyncMock()
    return mock_client


@pytest.fixture
def mock_local_storage_client():
    """Mock本地存储客户端"""
    mock_client = AsyncMock()
    mock_client.upload_file = AsyncMock(return_value="/tmp/tfboys/test_file.png")
    mock_client.download_file = AsyncMock(return_value=b"fake_file_content")
    mock_client.delete_file = AsyncMock()
    return mock_client


@pytest.fixture
def mock_qiniu_text_client():
    """Mock 七牛 AI 文本推理客户端"""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_choice = AsyncMock()
    mock_message = AsyncMock()
    mock_message.content = '{"scenes": []}'
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    return mock_client


@pytest.fixture
def mock_qiniu_image_client():
    """Mock 七牛文生图客户端"""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    # 七牛 API 返回 base64 或 URL 格式
    mock_data = AsyncMock()
    mock_data.url = "https://example.com/image.png"
    mock_response.data = [mock_data]
    mock_client.images.generate = AsyncMock(return_value=mock_response)
    mock_client.close = AsyncMock()
    return mock_client


@pytest.fixture
def sample_novel_text():
    """示例小说文本"""
    return """
    春天的早晨,校园里樱花盛开。小明走在林荫道上,看着花瓣飘落。
    他是一个黑色短发、蓝色眼睛的少年,身穿白色校服。
    阳光透过树叶洒在地面,微风吹过,带来花香。
    """


@pytest.fixture
def sample_scenes_data():
    """示例场景数据"""
    return [
        {
            "scene_index": 1,
            "description": "清晨的校园,樱花飘落,阳光透过树叶洒在地面",
            "narration": "春天的早晨,校园里樱花盛开,微风吹过,花瓣如雪般飘落。"
        },
        {
            "scene_index": 2,
            "description": "教室里,阳光从窗外照进来",
            "narration": "小明走进教室,同学们已经在座位上了。"
        }
    ]


@pytest.fixture
def mock_httpx_client():
    """Mock httpx客户端"""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.content = b"fake_content"
    mock_response.json = AsyncMock(return_value={"status": "success"})
    mock_response.raise_for_status = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.post = AsyncMock(return_value=mock_response)
    return mock_client
