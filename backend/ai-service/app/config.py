from pydantic_settings import BaseSettings
from pydantic import field_validator


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
    
    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("OPENAI_API_KEY is required for image generation")
        return v
    
    @field_validator("anthropic_api_key")
    @classmethod
    def validate_anthropic_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ANTHROPIC_API_KEY is required for text analysis")
        return v
    
    @field_validator("qiniu_access_key", "qiniu_secret_key")
    @classmethod
    def validate_qiniu_keys(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Qiniu TTS credentials are required")
        return v
    
    @field_validator("oss_access_key_id", "oss_access_key_secret", "oss_endpoint")
    @classmethod
    def validate_oss_config(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("OSS configuration is required")
        return v
    
    class Config:
        env_file = ".env"


settings = Settings()
