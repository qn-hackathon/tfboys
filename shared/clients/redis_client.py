"""
Redis 客户端 - 任务状态管理和角色库管理
"""
import redis.asyncio as redis
import json
from typing import Optional, List, Any
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis 客户端,用于任务状态管理和角色库管理"""
    
    def __init__(self, redis_url: str):
        """
        初始化 Redis 客户端
        
        Args:
            redis_url: Redis 连接 URL (如: redis://localhost:6379/0)
        """
        self.redis = redis.from_url(redis_url, decode_responses=True)
    
    async def get_task(self, task_id: str) -> Optional[dict]:
        """
        获取任务信息
        
        Args:
            task_id: 任务ID
            
        Returns:
            dict: 任务数据,如果不存在返回 None
        """
        try:
            data = await self.redis.get(f"task:{task_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Failed to get task {task_id}: {e}")
            raise
    
    async def save_task(self, task_id: str, task_data: dict, ttl: int = 604800):
        """
        保存任务信息
        
        Args:
            task_id: 任务ID
            task_data: 任务数据
            ttl: 过期时间(秒),默认7天
        """
        try:
            key = f"task:{task_id}"
            await self.redis.set(key, json.dumps(task_data), ex=ttl)
            await self.redis.sadd("tasks", task_id)
            logger.info(f"Task {task_id} saved successfully")
        except Exception as e:
            logger.error(f"Failed to save task {task_id}: {e}")
            raise
    
    async def update_task_status(self, task_id: str, status: str, error: Optional[str] = None):
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            error: 错误信息(可选)
        """
        try:
            task_data = await self.get_task(task_id)
            if task_data:
                task_data["status"] = status
                if error:
                    task_data["error"] = error
                await self.save_task(task_id, task_data)
        except Exception as e:
            logger.error(f"Failed to update task status {task_id}: {e}")
            raise
    
    async def list_tasks(self) -> List[dict]:
        """
        列出所有任务
        
        Returns:
            List[dict]: 任务列表
        """
        try:
            task_ids = await self.redis.smembers("tasks")
            tasks = []
            for task_id in task_ids:
                task_data = await self.get_task(task_id)
                if task_data:
                    tasks.append(task_data)
            return tasks
        except Exception as e:
            logger.error(f"Failed to list tasks: {e}")
            raise
    
    async def delete_task(self, task_id: str) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            result = await self.redis.delete(f"task:{task_id}")
            await self.redis.srem("tasks", task_id)
            return result > 0
        except Exception as e:
            logger.error(f"Failed to delete task {task_id}: {e}")
            return False
    
    async def save_character(self, character_id: str, character_data: dict):
        """
        保存角色信息到角色库
        
        Args:
            character_id: 角色ID
            character_data: 角色数据
        """
        try:
            key = f"character:{character_id}"
            await self.redis.set(key, json.dumps(character_data))
            logger.info(f"Character {character_id} saved successfully")
        except Exception as e:
            logger.error(f"Failed to save character {character_id}: {e}")
            raise
    
    async def get_character(self, character_id: str) -> Optional[dict]:
        """
        获取角色信息
        
        Args:
            character_id: 角色ID
            
        Returns:
            dict: 角色数据,如果不存在返回 None
        """
        try:
            data = await self.redis.get(f"character:{character_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Failed to get character {character_id}: {e}")
            raise
    
    async def list_task_characters(self, task_id: str) -> List[str]:
        """
        获取任务的所有角色ID
        
        Args:
            task_id: 任务ID
            
        Returns:
            List[str]: 角色ID列表
        """
        try:
            key = f"task:{task_id}:characters"
            character_ids = await self.redis.smembers(key)
            return list(character_ids)
        except Exception as e:
            logger.error(f"Failed to list task characters for {task_id}: {e}")
            raise
    
    async def add_task_character(self, task_id: str, character_id: str):
        """
        添加角色到任务的角色列表
        
        Args:
            task_id: 任务ID
            character_id: 角色ID
        """
        try:
            key = f"task:{task_id}:characters"
            await self.redis.sadd(key, character_id)
            logger.info(f"Character {character_id} added to task {task_id}")
        except Exception as e:
            logger.error(f"Failed to add character to task: {e}")
            raise
    
    async def set_value(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        设置键值对
        
        Args:
            key: 键
            value: 值
            ttl: 过期时间(秒),None表示不过期
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            if ttl:
                await self.redis.set(key, value, ex=ttl)
            else:
                await self.redis.set(key, value)
        except Exception as e:
            logger.error(f"Failed to set value for key {key}: {e}")
            raise
    
    async def get_value(self, key: str) -> Optional[str]:
        """
        获取键值
        
        Args:
            key: 键
            
        Returns:
            str: 值,如果不存在返回 None
        """
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error(f"Failed to get value for key {key}: {e}")
            raise
    
    async def close(self):
        """关闭 Redis 连接"""
        await self.redis.close()


redis_client: Optional[RedisClient] = None


def init_redis_client(redis_url: str) -> RedisClient:
    """
    初始化全局 Redis 客户端实例
    
    使用示例:
        from shared.clients import init_redis_client, redis_client
        
        init_redis_client("redis://localhost:6379/0")
        
        await redis_client.save_task("task_001", {"status": "pending"})
    """
    global redis_client
    redis_client = RedisClient(redis_url)
    return redis_client
