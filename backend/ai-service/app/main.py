from fastapi import FastAPI
from app.api import internal, callbacks

app = FastAPI(
    title="TFBoys AI Service",
    description="AI处理服务 - 文本分析、图像生成、配音生成",
    version="1.0.0"
)

app.include_router(internal.router, prefix="/internal", tags=["internal"])
app.include_router(callbacks.router, prefix="/callbacks", tags=["callbacks"])


@app.get("/")
def root():
    return {"message": "TFBoys AI Service", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
