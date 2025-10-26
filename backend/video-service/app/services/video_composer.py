"""
视频合成服务 - 使用FFmpeg合成视频
"""
from typing import List
from app.models.video_job import VideoJob
from app.models.scene import Scene
from app.models.video_config import VideoConfig
from app.utils.ffmpeg_builder import FFmpegCommandBuilder
from app.utils.file_utils import get_file_size
from .ffmpeg_executor import ffmpeg_executor
from .subtitle_renderer import SubtitleRenderer
from .local_storage_client import local_storage_client
from .resource_manager import resource_manager


class VideoComposer:
    def __init__(self):
        self.ffmpeg_executor = ffmpeg_executor
        self.local_storage_client = local_storage_client
        self.resource_manager = resource_manager
    
    async def compose_video(self, job: VideoJob) -> str:
        """
        完整视频合成流程
        
        Args:
            job: 视频任务对象
        
        Returns:
            视频URL
        """
        workspace = self.resource_manager.create_job_workspace(job.job_id)
        scene_videos = []
        
        try:
            for scene in job.scenes:
                image_path, audio_path = await self.resource_manager.download_scene_resources(
                    scene, workspace
                )
                
                scene_video_path = await self.compose_scene(
                    scene, job.video_config, image_path, audio_path, workspace
                )
                scene_videos.append(scene_video_path)
            
            final_video_path = await self.concat_scenes(scene_videos, workspace)
            
            object_key = f"videos/{job.task_id}.mp4"
            video_path = await self.local_storage_client.upload_file(final_video_path, object_key)
            
            return video_path
        
        finally:
            self.resource_manager.cleanup_workspace(workspace)
    
    async def compose_scene(
        self,
        scene: Scene,
        config: VideoConfig,
        image_path: str,
        audio_path: str,
        workspace: str
    ) -> str:
        """
        合成单个场景视频
        
        Args:
            scene: 场景对象
            config: 视频配置
            image_path: 图片路径
            audio_path: 音频路径
            workspace: 工作目录
        
        Returns:
            场景视频文件路径
        """
        subtitle_renderer = SubtitleRenderer(config.subtitle_style)
        subtitle_filter = subtitle_renderer.build_drawtext_filter(scene.subtitle_text)
        
        output_path = self.resource_manager.get_scene_output_path(
            workspace, scene.scene_index
        )
        
        command = FFmpegCommandBuilder.build_scene_video_command(
            image_path=image_path,
            audio_path=audio_path,
            subtitle_filter=subtitle_filter,
            output_path=output_path,
            duration=scene.duration
        )
        
        success, output = self.ffmpeg_executor.execute(command)
        
        if not success:
            raise Exception(f"Failed to compose scene {scene.scene_index}: {output}")
        
        return output_path
    
    async def concat_scenes(self, scene_videos: List[str], workspace: str) -> str:
        """
        拼接多个场景视频
        
        Args:
            scene_videos: 场景视频文件路径列表
            workspace: 工作目录
        
        Returns:
            最终视频文件路径
        """
        if len(scene_videos) == 1:
            return scene_videos[0]
        
        concat_file = self.resource_manager.get_concat_file_path(workspace)
        FFmpegCommandBuilder.create_concat_file(scene_videos, concat_file)
        
        output_path = self.resource_manager.get_final_output_path(workspace)
        
        command = FFmpegCommandBuilder.build_concat_command(
            scene_videos=scene_videos,
            output_path=output_path,
            concat_file=concat_file
        )
        
        success, output = self.ffmpeg_executor.execute(command)
        
        if not success:
            raise Exception(f"Failed to concat scenes: {output}")
        
        return output_path


video_composer = VideoComposer()
