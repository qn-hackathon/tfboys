"""
文本分析服务 - 使用GPT-4/Claude分析小说文本
"""
from typing import List, Dict
from openai import OpenAI
from app.config import settings


class TextAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def analyze_novel(self, novel_text: str) -> List[Dict]:
        """
        分析小说文本,分割场景并识别角色
        
        返回场景列表,每个场景包含:
        - scene_index: 场景索引
        - description: 场景描述
        - characters: 角色列表
        - narration: 旁白文字
        """
        prompt = f"""
        请分析以下小说文本,将其分割为多个场景,每个场景包含:
        1. 场景描述(用于生成图像)
        2. 出现的角色(包括角色特征描述)
        3. 旁白文字(用于配音)
        
        小说文本:
        {novel_text}
        
        请以JSON格式返回场景列表。
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "你是一个专业的小说场景分析专家。"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return []


text_analyzer = TextAnalyzer()
