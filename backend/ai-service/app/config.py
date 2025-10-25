from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    # 基础服务配置
    redis_url: str = "redis://localhost:6379/0"
    video_service_url: str = "http://localhost:8003"

    # 七牛 AI Token API 配置
    qiniu_api_key: str = ""  # 七牛 AI Token API Key (用于图像生成和文本分析)
    qiniu_access_key: str = ""  # 七牛 Access Key (用于 TTS)
    qiniu_secret_key: str = ""  # 七牛 Secret Key (用于 TTS)

    @field_validator("qiniu_api_key")
    @classmethod
    def validate_qiniu_api_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("QINIU_API_KEY is required for AI services")
        return v

    @field_validator("qiniu_access_key", "qiniu_secret_key")
    @classmethod
    def validate_qiniu_keys(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Qiniu TTS credentials are required")
        return v

    class Config:
        env_file = ".env"


settings = Settings()
