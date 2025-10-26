#!/bin/bash
# 启动开发环境

echo "启动Redis..."
docker-compose up -d redis

echo "等待Redis启动..."
sleep 2

echo "请在不同终端运行以下命令:"
echo ""
echo "终端1 - API Gateway:"
echo "  cd backend/api-gateway && uvicorn app.main:app --reload --port 8000"
echo ""
echo "终端2 - AI Service:"
echo "  cd backend/ai-service"
echo "  export PYTHONPATH=\$(cd ../.. && pwd)"
echo "  uvicorn app.main:app --reload --port 8001"
echo ""
echo "终端3 - Video Service:"
echo "  cd backend/video-service && uvicorn app.main:app --reload --port 8002"
echo ""
echo "终端4 - 前端:"
echo "  cd frontend && npm run dev"
