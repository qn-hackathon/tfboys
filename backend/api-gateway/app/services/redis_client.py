import redis.asyncio as redis
import json
from typing import Optional, List
from app.config import settings


class RedisClient:
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url, decode_responses=True)
    
    async def get_task(self, task_id: str) -> Optional[dict]:
        """获取任务信息"""
        data = await self.redis.get(f"task:{task_id}")
        if data:
            return json.loads(data)
        return None
    
    async def save_task(self, task_id: str, task_data: dict):
        """保存任务信息"""
        await self.redis.set(f"task:{task_id}", json.dumps(task_data))
        await self.redis.sadd("tasks", task_id)
    
    async def list_tasks(self) -> List[dict]:
        """列出所有任务"""
        task_ids = await self.redis.smembers("tasks")
        tasks = []
        for task_id in task_ids:
            task_data = await self.get_task(task_id)
            if task_data:
                tasks.append(task_data)
        return tasks
    
    async def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        result = await self.redis.delete(f"task:{task_id}")
        await self.redis.srem("tasks", task_id)
        return result > 0


redis_client = RedisClient()
