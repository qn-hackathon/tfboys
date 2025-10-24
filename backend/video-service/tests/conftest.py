import pytest


@pytest.fixture
def sample_scene_data():
    return {
        "scene_id": "scene_001",
        "scene_index": 1,
        "description": "测试场景",
        "narration": "这是一个测试场景",
        "characters": [],
        "image_url": "https://example.com/image.jpg",
        "audio_url": "https://example.com/audio.mp3",
        "audio_duration": 5.0,
        "subtitle_text": "测试字幕"
    }
