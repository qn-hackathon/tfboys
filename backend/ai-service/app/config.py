from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # 基础服务配置
    redis_url: str = "redis://localhost:6379/0"
    video_service_url: str = "http://localhost:8003"

    # 七牛 AI Token API 配置
    qiniu_api_key: str = ""  # 七牛 AI Token API Key (用于图像生成和文本分析)
    qiniu_access_key: str = ""  # 七牛 Access Key (用于 TTS)
    qiniu_secret_key: str = ""  # 七牛 Secret Key (用于 TTS)

    class Config:
        env_file = ".env"


# 创建设置实例
# 注意: 在测试环境下，允许空的 API keys
settings = Settings()
