from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    video_service_url: str = "http://localhost:8002"
    
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    midjourney_api_key: str = ""
    midjourney_api_url: str = "https://api.midjourney.com/v1"
    
    aliyun_tts_access_key: str = ""
    aliyun_tts_secret_key: str = ""
    aliyun_tts_app_key: str = ""
    
    oss_endpoint: str = ""
    oss_access_key: str = ""
    oss_secret_key: str = ""
    oss_bucket: str = "tfboys"
    
    class Config:
        env_file = ".env"


settings = Settings()
