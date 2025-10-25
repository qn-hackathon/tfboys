"""
角色管理服务 - 维护角色库,确保角色一致性
"""
from typing import Optional, Dict, List
import hashlib
import logging
import asyncio
from shared.clients.redis_client import redis_client
from shared.models.scene import Scene, Character
from app.services.image_generator import ImageGenerator

logger = logging.getLogger(__name__)


class CharacterManager:
    """
    角色管理器,负责:
    1. 角色提取与去重
    2. 角色设定图生成
    3. 角色库管理
    4. 角色一致性支持
    """
    
    def __init__(self):
        self.image_generator = ImageGenerator()
    
    async def process_characters(
        self, 
        task_id: str, 
        scenes: List[Scene]
    ) -> Dict[str, Character]:
        """
        处理场景中的角色:
        1. 提取所有角色并去重
        2. 检查角色库
        3. 为新角色生成设定图
        4. 保存到角色库和任务关联
        
        Args:
            task_id: 任务ID
            scenes: 场景列表
            
        Returns:
            Dict[character_name, Character]: 角色名称到角色对象的映射
        """
        logger.info(f"Processing characters for task {task_id}")
        
        characters_dict: Dict[str, Character] = {}
        
        for scene in scenes:
            for character in scene.characters:
                if character.name not in characters_dict:
                    characters_dict[character.name] = character
        
        logger.info(f"Found {len(characters_dict)} unique characters")
        
        character_tasks = [
            self.get_or_create_character(
                character_name=name,
                character_desc=character.description,
                task_id=task_id
            )
            for name, character in characters_dict.items()
        ]
        
        processed_characters = await asyncio.gather(*character_tasks)
        
        result = {char.name: char for char in processed_characters}
        
        logger.info(f"Characters processed successfully for task {task_id}")
        return result
    
    async def get_or_create_character(
        self,
        character_name: str,
        character_desc: str,
        task_id: str
    ) -> Character:
        """
        获取或创建角色:
        1. 查询全局角色库 (character:{character_id})
        2. 如果不存在,生成设定图并保存
        3. 关联到任务 (task:{task_id}:characters)
        
        Args:
            character_name: 角色名称
            character_desc: 角色描述
            task_id: 任务ID
            
        Returns:
            Character: 角色对象(包含 reference_image_url)
        """
        character_id = self.generate_character_id(character_name)
        
        existing_character = await redis_client.get_character(character_id)
        
        if existing_character:
            logger.info(f"Character {character_name} found in cache")
            character = Character(**existing_character)
        else:
            logger.info(f"Creating new character: {character_name}")
            
            reference_image_url = await self.generate_character_image(
                character_name=character_name,
                character_desc=character_desc
            )
            
            character = Character(
                character_id=character_id,
                name=character_name,
                description=character_desc,
                reference_image_url=reference_image_url,
                midjourney_cref_url=reference_image_url
            )
            
            await redis_client.save_character(character_id, character.model_dump())
        
        await redis_client.add_task_character(task_id, character_id)
        
        return character
    
    async def generate_character_image(
        self,
        character_name: str,
        character_desc: str
    ) -> str:
        """
        生成角色设定图 (Midjourney, 无 --cref)
        
        Args:
            character_name: 角色名称
            character_desc: 角色描述
            
        Returns:
            str: 角色设定图 URL
        """
        logger.info(f"Generating character design image for {character_name}")
        
        prompt = f"anime style, character design sheet, {character_name}, {character_desc}, white background"
        
        image_url = await self.image_generator.generate_image(
            prompt=prompt,
            character_ref_url=None,
            ar="1:1"
        )
        
        logger.info(f"Character image generated: {image_url}")
        return image_url
    
    async def get_character_references(
        self,
        character_names: List[str]
    ) -> Dict[str, str]:
        """
        批量获取角色参考图 URL (用于场景生成的 --cref)
        
        Args:
            character_names: 角色名称列表
            
        Returns:
            Dict[name, reference_url]: 角色名称到参考图 URL 的映射
        """
        if not character_names:
            return {}
        
        references = {}
        
        for name in character_names:
            character_id = self.generate_character_id(name)
            character_data = await redis_client.get_character(character_id)
            
            if character_data and character_data.get("reference_image_url"):
                references[name] = character_data["reference_image_url"]
            else:
                logger.warning(f"No reference image found for character: {name}")
        
        return references
    
    def generate_character_id(self, character_name: str) -> str:
        """
        基于角色名称生成唯一 ID
        使用 hash 确保同名角色共享同一设定图
        
        Args:
            character_name: 角色名称
            
        Returns:
            str: 角色ID (格式: char_{hash})
        """
        hash_value = hashlib.md5(character_name.encode()).hexdigest()[:8]
        return f"char_{hash_value}"
    
    async def get_character_by_name(self, character_name: str) -> Optional[Character]:
        """
        根据角色名称获取角色信息
        
        Args:
            character_name: 角色名称
            
        Returns:
            Optional[Character]: 角色对象,不存在返回 None
        """
        character_id = self.generate_character_id(character_name)
        character_data = await redis_client.get_character(character_id)
        
        if character_data:
            return Character(**character_data)
        return None
    
    async def list_task_characters(self, task_id: str) -> List[Character]:
        """
        获取任务的所有角色
        
        Args:
            task_id: 任务ID
            
        Returns:
            List[Character]: 角色列表
        """
        character_ids = await redis_client.list_task_characters(task_id)
        
        characters = []
        for character_id in character_ids:
            character_data = await redis_client.get_character(character_id)
            if character_data:
                characters.append(Character(**character_data))
        
        return characters


character_manager = CharacterManager()
