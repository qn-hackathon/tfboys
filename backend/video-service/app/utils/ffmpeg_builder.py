from typing import List
import os


class FFmpegCommandBuilder:
    @staticmethod
    def build_scene_video_command(
        image_path: str,
        audio_path: str,
        subtitle_filter: str,
        output_path: str,
        duration: float
    ) -> List[str]:
        command = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", image_path,
            "-i", audio_path,
            "-vf", subtitle_filter,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-t", str(duration),
            output_path
        ]
        return command
    
    @staticmethod
    def build_concat_command(
        scene_videos: List[str],
        output_path: str,
        concat_file: str
    ) -> List[str]:
        command = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path
        ]
        return command
    
    @staticmethod
    def build_thumbnail_command(
        video_path: str,
        output_path: str,
        timestamp: float = 1.0
    ) -> List[str]:
        command = [
            "ffmpeg",
            "-y",
            "-ss", str(timestamp),
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            output_path
        ]
        return command
    
    @staticmethod
    def create_concat_file(scene_videos: List[str], concat_file_path: str):
        with open(concat_file_path, 'w') as f:
            for video in scene_videos:
                abs_path = os.path.abspath(video)
                f.write(f"file '{abs_path}'\n")
