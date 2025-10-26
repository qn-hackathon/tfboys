from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    ai_service_url: str = "http://localhost:8002"  # AI Service 运行在 8002 端口

    class Config:
        env_file = ".env"


settings = Settings()
