.PHONY: help install dev build build-frontend clean test

help:
	@echo "TFBoys - 文字生成视频系统"
	@echo ""
	@echo "可用命令:"
	@echo "  make install        - 安装所有依赖"
	@echo "  make dev            - 启动开发环境"
	@echo "  make build          - 构建所有Docker镜像"
	@echo "  make build-frontend - 构建前端Docker镜像"
	@echo "  make up             - 启动所有服务(Docker)"
	@echo "  make down           - 停止所有服务"
	@echo "  make clean          - 清理临时文件"
	@echo "  make test           - 运行测试"

install:
	@echo "安装前端依赖..."
	cd frontend && npm install
	@echo "安装后端依赖..."
	cd backend/api-gateway && pip install -r requirements.txt
	cd backend/ai-service && pip install -r requirements.txt
	cd backend/video-service && pip install -r requirements.txt

dev:
	@echo "启动开发环境..."
	docker-compose up -d redis
	@echo "Redis已启动"
	@echo "请在不同终端运行:"
	@echo "  cd frontend && npm run dev"
	@echo "  cd backend/api-gateway && uvicorn app.main:app --reload --host 0.0.0.0 --port 8001"
	@echo "  cd backend/ai-service && uvicorn app.main:app --reload --host 0.0.0.0 --port 8002"
	@echo "  cd backend/video-service && uvicorn app.main:app --reload --host 0.0.0.0 --port 8003"

build:
	@echo "构建Docker镜像..."
	docker-compose build

build-frontend:
	@echo "构建前端Docker镜像..."
	docker-compose build frontend
	@echo "前端镜像构建完成!"

up:
	@echo "启动所有服务..."
	docker-compose up -d
	@echo "服务已启动!"
	@echo "  前端: http://localhost:3000"
	@echo "  API Gateway: http://localhost:8001"
	@echo "  AI Service: http://localhost:8002"
	@echo "  Video Service: http://localhost:8003"

down:
	@echo "停止所有服务..."
	docker-compose down

clean:
	@echo "清理临时文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

test:
	@echo "运行测试..."
	cd backend/api-gateway && pytest
	cd backend/ai-service && pytest
	cd backend/video-service && pytest
	cd frontend && npm test
