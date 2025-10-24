"""
Prompt 构建器 - 用于构建高质量的 AI Prompt
"""
from typing import List


class PromptBuilder:
    """Prompt 构建器"""
    
    @staticmethod
    def build_scene_analysis_prompt(novel_text: str) -> str:
        """
        构建场景分析的 Prompt
        
        Args:
            novel_text: 小说文本
            
        Returns:
            str: 用于 GPT-4/Claude 的 Prompt
        """
        return f"""你是一个专业的小说场景分析师。请将以下小说文本分析并拆分成适合制作动漫视频的场景。

小说文本:
{novel_text}

请按照以下 JSON 格式输出:
{{
  "scenes": [
    {{
      "scene_index": 0,
      "description": "详细的场景描述,适合用于 Midjourney 图像生成。要求:1)包含具体的环境、光线、氛围描述;2)如有角色,描述其外貌、表情、动作;3)使用动漫风格的描述语言",
      "narration": "该场景的旁白文字,用于生成配音。要求简洁、有感染力",
      "characters": [
        {{
          "name": "角色名称",
          "description": "详细的角色外貌描述,包括发型、服装、体型等,用于确保角色一致性"
        }}
      ]
    }}
  ]
}}

要求:
1. 每个场景应该是一个相对独立的画面
2. 场景描述要具体、生动,符合动漫风格
3. 角色描述要详细且一致,同一角色在不同场景中的描述应保持一致
4. 旁白要简洁,便于配音
5. 场景数量控制在 5-15 个之间
6. 只返回 JSON,不要其他文字
"""

    @staticmethod
    def build_character_prompt(character_name: str, character_desc: str) -> str:
        """
        构建角色图像生成的 Prompt (用于首次生成角色设定图)
        
        Args:
            character_name: 角色名称
            character_desc: 角色描述
            
        Returns:
            str: 用于 Midjourney 的 Prompt
        """
        return f"""anime style, character design sheet, {character_name}, {character_desc}, white background, high quality, detailed --ar 1:1 --niji 6"""
    
    @staticmethod
    def build_scene_prompt(
        scene_desc: str,
        characters: List[dict],
        use_cref: bool = False
    ) -> str:
        """
        构建场景图像生成的 Prompt
        
        Args:
            scene_desc: 场景描述
            characters: 角色列表
            use_cref: 是否使用角色参考 (--cref)
            
        Returns:
            str: 用于 Midjourney 的 Prompt
        """
        character_names = ", ".join([c["name"] for c in characters]) if characters else ""
        
        prompt = f"anime style, {scene_desc}"
        if character_names:
            prompt += f", featuring {character_names}"
        prompt += ", cinematic composition, high quality, detailed --ar 16:9 --niji 6"
        
        return prompt
    
    @staticmethod
    def build_character_extraction_prompt(novel_text: str) -> str:
        """
        构建角色提取的 Prompt
        
        Args:
            novel_text: 小说文本
            
        Returns:
            str: 用于提取角色的 Prompt
        """
        return f"""请从以下小说文本中提取所有主要角色的信息。

小说文本:
{novel_text}

请按照以下 JSON 格式输出:
{{
  "characters": [
    {{
      "name": "角色名称",
      "description": "详细的外貌描述,包括发型、发色、眼睛颜色、服装风格、体型等,用于生成角色设定图"
    }}
  ]
}}

要求:
1. 只提取主要角色(出场次数较多或对情节重要的角色)
2. 描述要详细且具体,适合用于动漫角色设定图生成
3. 使用动漫风格的描述语言
4. 只返回 JSON,不要其他文字
"""
