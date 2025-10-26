from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # 基础服务配置
    redis_url: str = "redis://localhost:6379/0"
    video_service_url: str = "http://localhost:8003"
    local_storage_dir: str = "/tmp/tfboys"  # 本地存储目录

    # 七牛 AI Token API 配置
    qiniu_api_key: str = ""  # 七牛 AI Token API Key (用于图像生成、文本分析和 TTS)

    class Config:
        env_file = ".env"


# 创建设置实例
# 注意: 在测试环境下，允许空的 API keys
settings = Settings()
