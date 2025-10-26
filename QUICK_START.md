# TFBoys 快速启动指南

本指南帮助你在 5 分钟内启动并测试 TFBoys 系统。

## ✅ 前置条件检查

```bash
# 检查 Python 版本 (需要 3.9+)
python3 --version

# 检查 Redis 是否运行
redis-cli ping  # 应该返回 PONG

# 如果 Redis 未运行，启动它
brew services start redis  # macOS
```

## 🚀 5 分钟快速启动

### 1. 安装 Shared 模块 (一次性)

```bash
cd /Users/jiangzhi/repo/tfboys/shared
pip install -e .
```

### 2. 启动 AI Service (需要 2 个终端)

**终端 1 - AI Service API**:
```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service
export PYTHONPATH="/Users/jiangzhi/repo/tfboys"
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

**终端 2 - Celery Worker**:
```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service
export PYTHONPATH="/Users/jiangzhi/repo/tfboys"
celery -A app.workers.celery_app worker --loglevel=info
```

### 3. 启动 API Gateway

**终端 3**:
```bash
cd /Users/jiangzhi/repo/tfboys/backend/api-gateway
export PYTHONPATH="/Users/jiangzhi/repo/tfboys"
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 4. 运行测试

**终端 4 - 测试 AI Service**:
```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service
./test_e2e.sh
```

**终端 5 - 测试 API Gateway**:
```bash
cd /Users/jiangzhi/repo/tfboys/backend/api-gateway
./test_e2e.sh
```

## 📝 重要修复说明

在本次会话中，我修复了以下关键问题：

### 1. ✅ Celery + Redis 兼容性问题
- **问题**: `wrong number of arguments for 'ping' command`
- **修复**: 降级 Redis 库到 4.6.0，添加 `health_check_interval: 0`
- **文件**: 
  - `backend/ai-service/requirements.txt`
  - `shared/setup.py`
  - `backend/ai-service/app/workers/celery_app.py`

### 2. ✅ Redis Client 初始化时机问题
- **问题**: 模块导入时 `redis_client = None`，导致 API 调用失败
- **修复**: 添加 `get_redis_client()` 动态获取函数
- **文件**:
  - `shared/clients/__init__.py`
  - `backend/ai-service/app/api/internal.py`
  - `backend/ai-service/app/api/callbacks.py`
  - `backend/ai-service/app/workers/tasks.py`
  - `backend/api-gateway/app/api/tasks.py`

### 3. ✅ LocalStorageClient 在子进程中未初始化
- **问题**: Celery prefork 模式下，子进程没有 LocalStorageClient
- **修复**: 添加 `task_prerun` 信号，在每个任务前检查并初始化
- **文件**: `backend/ai-service/app/workers/celery_app.py`

### 4. ✅ Video Client 初始化问题
- **问题**: `video_client` 在子进程中是 `None`
- **修复**: 添加 `get_video_client()` 动态获取函数
- **文件**:
  - `backend/ai-service/app/services/video_client.py`
  - `backend/ai-service/app/workers/tasks.py`
  - `backend/ai-service/app/workers/celery_app.py`

### 5. ✅ Celery 任务未注册
- **问题**: Worker 启动时未自动发现任务
- **修复**: 添加 `imports=['app.workers.tasks']` 配置
- **文件**: `backend/ai-service/app/workers/celery_app.py`

### 6. ✅ 端口配置错误
- **问题**: 多处配置使用错误的端口号
- **修复**: 统一 AI Service 端口为 8002
- **文件**:
  - `backend/ai-service/test_e2e.sh`
  - `backend/ai-service/start_all.sh`
  - `backend/ai-service/QUICKSTART.md`
  - `backend/api-gateway/app/config.py`

## 🎯 服务端口总览

| 服务 | 端口 | 用途 |
|------|------|------|
| API Gateway | 8001 | 用户请求入口 |
| AI Service | 8002 | AI 处理服务 |
| Video Service | 8003 | 视频合成服务 |
| Redis | 6379 | 数据存储和消息队列 |

## 🧪 验证服务状态

```bash
# 检查所有服务
curl http://localhost:8001/health  # API Gateway
curl http://localhost:8002/health  # AI Service
redis-cli ping                      # Redis

# 查看 Celery Worker 状态
ps aux | grep celery
```

## 📚 完整文档

- **完整部署指南**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **项目开发指南**: [CLAUDE.md](CLAUDE.md)
- **AI Service 测试指南**: [backend/ai-service/E2E_TESTING.md](backend/ai-service/E2E_TESTING.md)

## ⚠️ 常见问题

### Celery Worker 报错

如果遇到 Redis 相关错误：
```bash
pip install redis==4.6.0
cd /Users/jiangzhi/repo/tfboys/shared && pip install -e .
pkill -f "celery.*worker"
# 然后重新启动 Worker
```

### 任务一直 pending

确保 Celery Worker 正在运行并且日志中显示：
```
[tasks]
  . process_novel_task
```

### Redis client not initialized

重启相关服务，确保启动时看到 "Redis client initialized" 日志。

## 🎉 开始使用

现在你可以通过 API Gateway 创建任务了：

```bash
curl -X POST http://localhost:8001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "novel_text": "小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸。"
  }'
```

祝你使用愉快！🚀
