from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    temp_dir: str = "/tmp/video-service"
    ffmpeg_threads: int = 4
    chinese_font_path: str = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    ai_service_callback_url: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()
