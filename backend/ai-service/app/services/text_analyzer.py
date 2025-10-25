"""
文本分析服务 - 使用GPT-4/Claude分析小说文本
"""
from typing import List, Dict
import json
import logging
import asyncio
from anthropic import Anthropic
from app.config import settings
from shared.exceptions import TextAnalysisException

logger = logging.getLogger(__name__)


class TextAnalyzer:
    """文本分析器,将小说文本分割为场景并识别角色"""
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
    
    async def analyze_novel(self, novel_text: str) -> List[Dict]:
        """
        分析小说文本,分割场景并识别角色
        
        Args:
            novel_text: 小说文本内容
        
        Returns:
            List[Dict]: 场景列表,每个场景包含:
                - scene_index: 场景索引 (int)
                - description: 场景描述 (str) - 用于图像生成
                - narration: 旁白文字 (str) - 用于配音
                - characters: 角色列表 (List[Dict])
                    - name: 角色名称 (str)
                    - description: 角色外貌特征描述 (str)
        """
        logger.info(f"Analyzing novel text ({len(novel_text)} characters)...")
        
        try:
            prompt = self._build_prompt(novel_text)
            
            response = await asyncio.to_thread(
                self.client.messages.create,
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result_text = response.content[0].text
            result = json.loads(result_text)
            
            scenes = result.get("scenes", [])
            
            scenes = self._normalize_character_descriptions(scenes)
            
            logger.info(f"Successfully analyzed {len(scenes)} scenes")
            
            return scenes
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}", exc_info=True)
            raise TextAnalysisException(f"Invalid JSON response from Claude: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to analyze novel: {str(e)}", exc_info=True)
            raise TextAnalysisException(str(e))
    
    def _build_prompt(self, novel_text: str) -> str:
        """构建分析提示词"""
        text_length = len(novel_text)
        if text_length < 500:
            suggested_scenes = "2-5个场景"
        elif text_length < 2000:
            suggested_scenes = "5-10个场景"
        else:
            suggested_scenes = "10-20个场景"
        
        return f"""
你是一个专业的小说场景分析专家,擅长将小说文本分割为适合视频制作的场景。

请分析以下小说文本,将其分割为多个适合制作动漫视频的场景。

分析要求:
1. 每个场景应该是一个相对完整的画面或情节片段
2. 场景描述要具体、视觉化,便于图像生成
3. 识别场景中出现的角色,并描述其外貌特征(同一角色在不同场景中的描述必须完全一致)
4. 提取旁白文字,用于后续配音

小说文本:
{novel_text}

请以JSON格式返回,格式如下:
{{
  "scenes": [
    {{
      "scene_index": 1,
      "description": "清晨的校园,樱花飘落,阳光透过树叶洒在地面",
      "narration": "春天的早晨,校园里樱花盛开,微风吹过,花瓣如雪般飘落。",
      "characters": [
        {{
          "name": "小明",
          "description": "少年,黑色短发,蓝色眼睛,身穿白色校服"
        }}
      ]
    }}
  ]
}}

注意:
- scene_index 从 1 开始
- description 要详细描述场景环境、氛围、视觉元素
- narration 是配音文本,要流畅自然
- characters 列表中每个角色要包含 name 和 description
- 同一角色的 description 必须在所有场景中保持完全一致
- 建议生成{suggested_scenes}
- 只返回JSON,不要包含其他文字说明
"""
    
    def _normalize_character_descriptions(self, scenes: List[Dict]) -> List[Dict]:
        """
        归一化角色描述,确保同名角色描述一致
        
        Args:
            scenes: 场景列表
            
        Returns:
            List[Dict]: 归一化后的场景列表
        """
        characters_dict = {}
        
        for scene in scenes:
            for char in scene.get("characters", []):
                char_name = char.get("name")
                if char_name and char_name not in characters_dict:
                    characters_dict[char_name] = char.get("description", "")
        
        for scene in scenes:
            for char in scene.get("characters", []):
                char_name = char.get("name")
                if char_name and char_name in characters_dict:
                    char["description"] = characters_dict[char_name]
        
        return scenes


text_analyzer = TextAnalyzer()
