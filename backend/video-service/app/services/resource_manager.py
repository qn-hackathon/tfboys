import os
from typing import List
from app.models.scene import Scene
from app.utils.file_utils import ensure_dir, cleanup_files
from .oss_client import oss_client


class ResourceManager:
    def __init__(self, temp_dir: str = "/tmp/video-service"):
        self.temp_dir = temp_dir
        ensure_dir(temp_dir)
    
    def create_job_workspace(self, job_id: str) -> str:
        workspace = os.path.join(self.temp_dir, job_id)
        ensure_dir(workspace)
        ensure_dir(os.path.join(workspace, "images"))
        ensure_dir(os.path.join(workspace, "audio"))
        ensure_dir(os.path.join(workspace, "scenes"))
        return workspace
    
    async def download_scene_resources(self, scene: Scene, workspace: str) -> tuple[str, str]:
        image_path = os.path.join(workspace, "images", f"scene_{scene.scene_index}.jpg")
        audio_path = os.path.join(workspace, "audio", f"scene_{scene.scene_index}.mp3")
        
        await oss_client.download_file(scene.image_url, image_path)
        await oss_client.download_file(scene.audio_url, audio_path)
        
        return image_path, audio_path
    
    def cleanup_workspace(self, workspace: str):
        cleanup_files([workspace])
    
    def get_scene_output_path(self, workspace: str, scene_index: int) -> str:
        return os.path.join(workspace, "scenes", f"scene_{scene_index}.mp4")
    
    def get_final_output_path(self, workspace: str) -> str:
        return os.path.join(workspace, "final_video.mp4")
    
    def get_concat_file_path(self, workspace: str) -> str:
        return os.path.join(workspace, "concat_list.txt")


resource_manager = ResourceManager()
