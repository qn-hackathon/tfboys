"""
测试文本分析服务
"""
import pytest
import json
from unittest.mock import patch, AsyncMock
from app.services.text_analyzer import TextAnalyzer
from shared.exceptions import TextAnalysisException


@pytest.mark.unit
class TestTextAnalyzer:
    @pytest.fixture
    def text_analyzer(self, mock_qiniu_text_client):
        """创建TextAnalyzer实例"""
        with patch('app.services.text_analyzer.AsyncOpenAI', return_value=mock_qiniu_text_client):
            analyzer = TextAnalyzer()
            return analyzer

    @pytest.mark.asyncio
    async def test_analyze_novel_success(self, text_analyzer, sample_novel_text, sample_scenes_data):
        """测试成功分析小说"""
        # Mock 七牛 AI 响应格式
        mock_response = AsyncMock()
        mock_choice = AsyncMock()
        mock_message = AsyncMock()
        mock_message.content = json.dumps({"scenes": sample_scenes_data})
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        text_analyzer.client.chat.completions.create = AsyncMock(return_value=mock_response)

        scenes = await text_analyzer.analyze_novel(sample_novel_text)

        assert len(scenes) == 2
        assert scenes[0]["scene_index"] == 1
        assert scenes[0]["characters"][0]["name"] == "小明"

    @pytest.mark.asyncio
    async def test_analyze_novel_invalid_json(self, text_analyzer, sample_novel_text):
        """测试无效JSON响应"""
        mock_response = AsyncMock()
        mock_choice = AsyncMock()
        mock_message = AsyncMock()
        mock_message.content = "invalid json"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        text_analyzer.client.chat.completions.create = AsyncMock(return_value=mock_response)

        with pytest.raises(TextAnalysisException, match="Invalid JSON response"):
            await text_analyzer.analyze_novel(sample_novel_text)

    @pytest.mark.asyncio
    async def test_analyze_novel_api_error(self, text_analyzer, sample_novel_text):
        """测试API调用失败"""
        text_analyzer.client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

        with pytest.raises(TextAnalysisException, match="API Error"):
            await text_analyzer.analyze_novel(sample_novel_text)
    
    def test_build_prompt_short_text(self, text_analyzer):
        """测试短文本提示词生成"""
        short_text = "短文本" * 50
        prompt = text_analyzer._build_prompt(short_text)
        
        assert "2-5个场景" in prompt
        assert short_text in prompt
    
    def test_build_prompt_medium_text(self, text_analyzer):
        """测试中等文本提示词生成"""
        medium_text = "中等文本" * 200
        prompt = text_analyzer._build_prompt(medium_text)
        
        assert "5-10个场景" in prompt
    
    def test_build_prompt_long_text(self, text_analyzer):
        """测试长文本提示词生成"""
        long_text = "长文本" * 1000  # 增加到1000以超过2000字符
        prompt = text_analyzer._build_prompt(long_text)

        assert "10-20个场景" in prompt
    
    def test_normalize_character_descriptions(self, text_analyzer):
        """测试角色描述归一化"""
        scenes = [
            {
                "characters": [
                    {"name": "小明", "description": "黑发少年"},
                    {"name": "小红", "description": "红发少女"}
                ]
            },
            {
                "characters": [
                    {"name": "小明", "description": "黑发少年"},
                    {"name": "小红", "description": "不同的描述"}
                ]
            }
        ]
        
        normalized = text_analyzer._normalize_character_descriptions(scenes)
        
        assert normalized[0]["characters"][0]["description"] == "黑发少年"
        assert normalized[1]["characters"][0]["description"] == "黑发少年"
        assert normalized[0]["characters"][1]["description"] == "红发少女"
        assert normalized[1]["characters"][1]["description"] == "红发少女"
