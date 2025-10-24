from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    ai_service_url: str = "http://localhost:8001"
    
    class Config:
        env_file = ".env"


settings = Settings()
