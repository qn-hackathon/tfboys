"""
FFmpeg命令执行器
"""
import subprocess
from typing import List


class FFmpegExecutor:
    @staticmethod
    def execute(command: List[str]) -> bool:
        """
        执行FFmpeg命令
        
        Args:
            command: FFmpeg命令列表
        
        Returns:
            是否成功
        """
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr}")
            return False


ffmpeg_executor = FFmpegExecutor()
