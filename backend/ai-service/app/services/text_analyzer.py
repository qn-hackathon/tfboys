"""
文本分析服务 - 使用GPT-4/Claude分析小说文本
"""
from typing import List, Dict
import json
import logging
from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)


class TextAnalyzer:
    """文本分析器,将小说文本分割为场景并识别角色"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def analyze_novel(self, novel_text: str) -> List[Dict]:
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
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system", 
                        "content": "你是一个专业的小说场景分析专家,擅长将小说文本分割为适合视频制作的场景。"
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            scenes = result.get("scenes", [])
            logger.info(f"Successfully analyzed {len(scenes)} scenes")
            
            return scenes
            
        except Exception as e:
            logger.error(f"Failed to analyze novel: {str(e)}", exc_info=True)
            return self._get_fallback_scenes(novel_text)
    
    def _build_prompt(self, novel_text: str) -> str:
        """构建分析提示词"""
        return f"""
请分析以下小说文本,将其分割为多个适合制作动漫视频的场景。

分析要求:
1. 每个场景应该是一个相对完整的画面或情节片段
2. 场景描述要具体、视觉化,便于图像生成
3. 识别场景中出现的角色,并描述其外貌特征
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
- 尽量提取3-10个场景,不要太少也不要太多
"""
    
    def _get_fallback_scenes(self, novel_text: str) -> List[Dict]:
        """
        当API调用失败时,返回一个基础场景
        这是一个临时方案,实际生产环境需要更好的容错机制
        """
        logger.warning("Using fallback scene generation")
        
        text_preview = novel_text[:200] if len(novel_text) > 200 else novel_text
        
        return [
            {
                "scene_index": 1,
                "description": f"故事场景,{text_preview}",
                "narration": text_preview,
                "characters": [
                    {
                        "name": "主角",
                        "description": "年轻人,普通装扮"
                    }
                ]
            }
        ]


text_analyzer = TextAnalyzer()
