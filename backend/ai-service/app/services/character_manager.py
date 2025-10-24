"""
角色管理服务 - 维护角色库,确保角色一致性
"""
from typing import Optional, Dict
import redis.asyncio as redis
import json
from app.config import settings


class CharacterManager:
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url, decode_responses=True)
    
    async def get_character(self, task_id: str, character_name: str) -> Optional[Dict]:
        """获取角色信息"""
        key = f"character:{task_id}:{character_name}"
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None
    
    async def save_character(self, task_id: str, character_name: str, character_data: Dict):
        """保存角色信息"""
        key = f"character:{task_id}:{character_name}"
        await self.redis.set(key, json.dumps(character_data))


character_manager = CharacterManager()
