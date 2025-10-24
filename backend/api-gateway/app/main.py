from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import tasks, health


app = FastAPI(
    title="TFBoys API Gateway",
    description="文字生成视频系统 API网关",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(health.router, tags=["health"])


@app.get("/")
def root():
    return {"message": "TFBoys API Gateway", "version": "1.0.0"}
