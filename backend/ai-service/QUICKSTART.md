# AI Service 快速启动指南

## 🎯 5分钟快速开始

### 步骤 1: 配置环境

```bash
cd backend/ai-service

# 创建环境配置文件
cat > .env << 'EOF'
QINIU_API_KEY=your-qiniu-api-key
REDIS_URL=redis://localhost:6379/0
VIDEO_SERVICE_URL=http://localhost:8003
EOF

# 将 your-qiniu-api-key 替换为真实的 API Key
```

### 步骤 2: 启动服务（需要3个终端）

#### 终端 1: Redis
```bash
docker-compose up -d redis
```

#### 终端 2: AI Service API
```bash
cd backend/ai-service
export PYTHONPATH="$(cd ../.. && pwd)"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

#### 终端 3: Celery Worker
```bash
cd backend/ai-service
export PYTHONPATH="$(cd ../.. && pwd)"
celery -A app.workers.celery_app worker --loglevel=info
```

### 步骤 3: 测试服务

在新的终端中运行：

```bash
cd backend/ai-service
./test_e2e.sh
```

## 📚 更多信息

- **完整测试指南**: [E2E_TESTING.md](./E2E_TESTING.md)
- **API 文档**: http://localhost:8002/docs
- **开发文档**: [README.md](./README.md)

## ⚠️ 常见问题

### Celery Worker 报错: "wrong number of arguments for 'ping' command"

**解决方案**:

1. 检查 Redis 库版本（应该是 4.6.0）:
   ```bash
   pip show redis
   ```

2. 如果是 5.x 版本，降级:
   ```bash
   pip install redis==4.6.0
   cd ../../shared && pip install -e .
   ```

3. 清理 Redis 缓存:
   ```bash
   redis-cli DEL _kombu.binding.celery
   ```

4. 重启 Celery Worker

