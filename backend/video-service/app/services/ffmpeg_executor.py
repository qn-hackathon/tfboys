"""
FFmpeg命令执行器
"""
import subprocess
import shutil
from typing import List


class FFmpegExecutor:
    @staticmethod
    def execute(command: List[str], timeout: int = 300) -> tuple[bool, str]:
        """
        执行FFmpeg命令
        
        Args:
            command: FFmpeg命令列表
            timeout: 超时时间(秒)
        
        Returns:
            (是否成功, 输出/错误信息)
        """
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"FFmpeg error: {e.stderr}"
            print(error_msg)
            return False, error_msg
        except subprocess.TimeoutExpired as e:
            error_msg = f"FFmpeg timeout after {timeout}s"
            print(error_msg)
            return False, error_msg
    
    @staticmethod
    def check_ffmpeg_installed() -> bool:
        """
        检查FFmpeg是否安装
        """
        return shutil.which("ffmpeg") is not None


ffmpeg_executor = FFmpegExecutor()
