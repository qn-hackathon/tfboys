import subprocess
import json
from typing import Dict


def get_audio_duration(audio_path: str) -> float:
    try:
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            audio_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return 0.0


def get_video_info(video_path: str) -> Dict:
    try:
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration:stream=width,height,r_frame_rate",
            "-of", "json",
            video_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        video_stream = next((s for s in data.get("streams", []) if s.get("width")), {})
        
        return {
            "duration": float(data.get("format", {}).get("duration", 0)),
            "width": video_stream.get("width", 0),
            "height": video_stream.get("height", 0),
            "fps": video_stream.get("r_frame_rate", "30/1")
        }
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {}


def generate_thumbnail(video_path: str, output_path: str, timestamp: float = 1.0):
    from .ffmpeg_builder import FFmpegCommandBuilder
    from ..services.ffmpeg_executor import ffmpeg_executor
    
    command = FFmpegCommandBuilder.build_thumbnail_command(
        video_path, output_path, timestamp
    )
    success, _ = ffmpeg_executor.execute(command)
    return success
