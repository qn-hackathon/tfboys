from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    video_service_url: str = "http://localhost:8003"
    
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    qiniu_access_key: str = ""
    qiniu_secret_key: str = ""
    
    oss_endpoint: str = ""
    oss_access_key_id: str = ""
    oss_access_key_secret: str = ""
    oss_bucket_name: str = "tfboys"
    
    class Config:
        env_file = ".env"


settings = Settings()
