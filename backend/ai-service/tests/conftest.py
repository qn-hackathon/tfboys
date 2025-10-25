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
    mock_client.get_character = AsyncMock(return_value=None)
    mock_client.save_character = AsyncMock()
    mock_client.add_task_character = AsyncMock()
    mock_client.list_task_characters = AsyncMock(return_value=[])
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
def mock_anthropic_client():
    """Mock Anthropic客户端"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='{"scenes": []}')]
    mock_client.messages.create = MagicMock(return_value=mock_response)
    return mock_client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI客户端"""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.data = [AsyncMock(url="https://example.com/image.png")]
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
            "narration": "春天的早晨,校园里樱花盛开,微风吹过,花瓣如雪般飘落。",
            "characters": [
                {
                    "name": "小明",
                    "description": "少年,黑色短发,蓝色眼睛,身穿白色校服"
                }
            ]
        },
        {
            "scene_index": 2,
            "description": "教室里,阳光从窗外照进来",
            "narration": "小明走进教室,同学们已经在座位上了。",
            "characters": [
                {
                    "name": "小明",
                    "description": "少年,黑色短发,蓝色眼睛,身穿白色校服"
                }
            ]
        }
    ]


@pytest.fixture
def sample_character_data():
    """示例角色数据"""
    return {
        "character_id": "char_12345678",
        "name": "小明",
        "description": "少年,黑色短发,蓝色眼睛,身穿白色校服",
        "reference_image_url": "/tmp/tfboys/characters/小明.png"
    }


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
