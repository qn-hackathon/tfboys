from fastapi import FastAPI

app = FastAPI(
    title="TFBoys Video Service",
    description="视频合成服务 - FFmpeg视频合成",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "TFBoys Video Service", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
