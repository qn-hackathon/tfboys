from fastapi import FastAPI
from app.api import internal

app = FastAPI(
    title="TFBoys Video Service",
    description="视频合成服务 - FFmpeg视频合成",
    version="1.0.0"
)

app.include_router(internal.router, prefix="/internal", tags=["internal"])


@app.get("/")
def root():
    return {"message": "TFBoys Video Service", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
