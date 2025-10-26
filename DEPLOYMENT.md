# TFBoys 系统部署指南

本文档提供 TFBoys 文字生成视频系统的完整部署和测试指南。

## 📋 系统架构

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│   前端      │─────→│ API Gateway  │─────→│ AI Service   │
│ (端口 3000) │      │  (端口 8001) │      │  (端口 8002) │
└─────────────┘      └──────────────┘      └──────────────┘
                             │                      │
                             ↓                      ↓
                       ┌──────────┐          ┌─────────────┐
                       │  Redis   │←─────────│Celery Worker│
                       │(端口 6379)│          └─────────────┘
                       └──────────┘                  │
                                                     ↓
                                              ┌──────────────┐
                                              │Video Service │
                                              │  (端口 8003) │
                                              └──────────────┘
```

## 🔧 服务说明

### 1. API Gateway (端口 8001)

- **功能**: 用户请求入口，转发请求到后端服务
- **路由**:
  - `POST /api/tasks` - 创建视频生成任务
  - `GET /api/tasks/{task_id}` - 获取任务详情
  - `GET /api/tasks` - 获取任务列表
  - `DELETE /api/tasks/{task_id}` - 删除任务
  - `GET /health` - 健康检查

### 2. AI Service (端口 8002)

- **功能**: AI 处理服务（文本分析、图像生成、配音生成）
- **内部路由**:
  - `POST /internal/tasks` - 创建 AI 处理任务
  - `GET /internal/tasks/{task_id}` - 获取任务状态
  - `POST /callbacks/video-completed` - 视频完成回调
  - `GET /health` - 健康检查

### 3. Video Service (端口 8003)

- **功能**: 视频合成服务
- **内部路由**:
  - `POST /internal/video-synthesis/jobs` - 提交视频合成任务
  - `GET /internal/status/{task_id}` - 获取合成状态

### 4. Redis (端口 6379)

- **功能**: 任务状态管理、消息队列

### 5. Celery Worker

- **功能**: 异步任务处理
- **任务**: `process_novel_task` - 处理小说生成视频的完整流程

## 📦 前置要求

### 系统要求

- Python 3.9+
- Redis
- Node.js 16+ (前端)
- 至少 4GB RAM

### Python 依赖

所有后端服务共享以下核心依赖：

- FastAPI
- Celery
- Redis (Python 客户端)
- httpx
- Pydantic

## 🚀 部署步骤

### 步骤 1: 安装 Shared 模块

```bash
cd /Users/jiangzhi/repo/tfboys/shared
pip install -e .
```

### 步骤 2: 启动 Redis

```bash
# macOS (使用 Homebrew)
brew services start redis

# 或使用 Docker
docker run -d --name redis -p 6379:6379 redis:latest

# 验证
redis-cli ping  # 应该返回 PONG
```

### 步骤 3: 启动 AI Service

**终端 1 - AI Service API**:

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service
export PYTHONPATH="/Users/jiangzhi/repo/tfboys"

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 QINIU_API_KEY

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

**终端 2 - Celery Worker**:

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service
export PYTHONPATH="/Users/jiangzhi/repo/tfboys"

# 启动 Worker
celery -A app.workers.celery_app worker --loglevel=info
```

**验证**:

```bash
# 检查 AI Service
curl http://localhost:8002/health

# 应该返回: {"status":"healthy"}
```

### 步骤 4: 启动 API Gateway

**终端 3 - API Gateway**:

```bash
cd /Users/jiangzhi/repo/tfboys/backend/api-gateway
export PYTHONPATH="/Users/jiangzhi/repo/tfboys"

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**验证**:

```bash
# 检查 API Gateway
curl http://localhost:8001/health

# 应该返回: {"status":"healthy"}
```

### 步骤 5: 启动 Video Service (可选)

如果需要完整的视频合成功能：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/video-service
export PYTHONPATH="/Users/jiangzhi/repo/tfboys"

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
```

## 🧪 测试

### 测试 AI Service

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service
./test_e2e.sh
```

**预期结果**:

- ✅ AI Service 健康检查通过
- ✅ 任务创建成功
- ✅ 文本分析完成
- ✅ 图像生成成功
- ✅ 配音生成成功
- ❌ 视频服务提交失败（如果未启动 Video Service）

### 测试 API Gateway

```bash
cd /Users/jiangzhi/repo/tfboys/backend/api-gateway
./test_e2e.sh
```

**预期结果**:

- ✅ API Gateway 健康检查通过
- ✅ AI Service 健康检查通过
- ✅ 任务创建成功（通过 Gateway）
- ✅ 获取任务详情成功
- ✅ 获取任务列表成功
- ✅ CORS 配置正确

### 手动测试完整流程

```bash
# 1. 创建任务
curl -X POST http://localhost:8001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "novel_text": "小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。"
  }'

# 记录返回的 task_id

# 2. 查询任务状态
curl http://localhost:8001/api/tasks/{task_id}

# 3. 查看所有任务
curl http://localhost:8001/api/tasks
```

## 🔍 故障排查

### 1. Celery Worker 报错: "wrong number of arguments for 'ping' command"

**解决方案**:

```bash
# 检查 Redis 库版本
pip show redis

# 应该是 4.6.0，如果不是，降级：
pip install redis==4.6.0
cd /Users/jiangzhi/repo/tfboys/shared && pip install -e .

# 重启 Celery Worker
```

### 2. Redis client not initialized

**原因**: FastAPI 应用未正确初始化 Redis 客户端

**检查**:

```bash
# 查看服务启动日志
# 应该看到: "Redis client initialized"
```

### 3. 任务一直处于 pending 状态

**可能原因**:

- Celery Worker 未启动
- Worker 未注册任务

**检查**:

```bash
# 查看 Worker 日志
# 应该看到:
# [tasks]
#   . process_novel_task
```

### 4. API Gateway 无法连接 AI Service

**检查配置**:

```bash
# 确认 AI Service URL 配置正确
# backend/api-gateway/app/config.py
# ai_service_url = "http://localhost:8002"  # 不是 8001！
```

### 5. LocalStorageClient not initialized

**解决方案**:

- 确保 Celery Worker 已重启并加载最新代码
- 检查 Worker 日志，确认 `task_prerun` 信号触发

## 📊 监控和日志

### 查看服务状态

```bash
# 检查所有服务
curl http://localhost:8001/health  # API Gateway
curl http://localhost:8002/health  # AI Service
curl http://localhost:8003/health  # Video Service (可选)
redis-cli ping                      # Redis
```

### 查看 Redis 数据

```bash
# 查看所有任务
redis-cli KEYS "task:*"

# 查看特定任务
redis-cli GET "task:your_task_id"

# 查看任务数量
redis-cli DBSIZE
```

### Celery Worker 监控

```bash
# 查看 Worker 进程
ps aux | grep celery

# 查看任务队列
redis-cli LLEN celery

# 使用 Flower 监控 (可选)
pip install flower
celery -A app.workers.celery_app flower --port=5555
# 访问 http://localhost:5555
```

## 🔐 环境变量配置

### AI Service (.env)

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# Video Service
VIDEO_SERVICE_URL=http://localhost:8003

# 七牛 AI Token API
QINIU_API_KEY=your-qiniu-api-key-here
```

### API Gateway (.env)

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# AI Service
AI_SERVICE_URL=http://localhost:8002
```

## 📝 API 端点总览

### API Gateway (用户端点)

| 方法   | 端点                   | 描述             |
| ------ | ---------------------- | ---------------- |
| POST   | `/api/tasks`           | 创建视频生成任务 |
| GET    | `/api/tasks/{task_id}` | 获取任务详情     |
| GET    | `/api/tasks`           | 获取任务列表     |
| DELETE | `/api/tasks/{task_id}` | 删除任务         |
| GET    | `/health`              | 健康检查         |

### AI Service (内部端点)

| 方法 | 端点                         | 描述             |
| ---- | ---------------------------- | ---------------- |
| POST | `/internal/tasks`            | 创建 AI 处理任务 |
| GET  | `/internal/tasks/{task_id}`  | 获取任务状态     |
| POST | `/callbacks/video-completed` | 视频完成回调     |
| GET  | `/health`                    | 健康检查         |

## 🎯 性能优化

### Celery Worker 配置

```bash
# 增加并发数
celery -A app.workers.celery_app worker --concurrency=16

# 使用不同的池类型
celery -A app.workers.celery_app worker --pool=gevent
```

### Redis 优化

```bash
# 设置 Redis 最大内存
redis-cli CONFIG SET maxmemory 2gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

## 📚 相关文档

- [项目开发指南](CLAUDE.md)
- [AI Service 测试指南](backend/ai-service/E2E_TESTING.md)
- [AI Service 快速启动](backend/ai-service/QUICKSTART.md)
- [架构文档](README.md)

## 🆘 获取帮助

如果遇到问题：

1. 查看相关服务的日志
2. 检查 Redis 连接状态
3. 验证环境变量配置
4. 查看 [故障排查](#🔍-故障排查) 部分
5. 提交 Issue 到 GitHub 仓库

---

**最后更新**: 2025-10-26
**维护者**: TFBoys Team
