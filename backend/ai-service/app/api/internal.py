from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import uuid
from datetime import datetime
from app.workers.tasks import process_novel_task

router = APIRouter()


class CreateTaskRequest(BaseModel):
    novel_text: str


@router.post("/tasks")
async def create_task(request: CreateTaskRequest, background_tasks: BackgroundTasks):
    """创建AI处理任务"""
    task_id = str(uuid.uuid4())
    
    background_tasks.add_task(process_novel_task.delay, task_id, request.novel_text)
    
    return {
        "task_id": task_id,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
