# AI Service Docker 快速启动指南

## 🎯 一键启动（最快 5 分钟）

### 前置条件

- Docker 和 Docker Compose 已安装
- 七牛 AI Token API Key（[获取方式](https://portal.qiniu.com/kodo/ak-sk)）

### 快速启动步骤

```bash
# 1. 配置环境变量
cd backend/ai-service
cp .env.example .env
nano .env  # 设置 QINIU_API_KEY

# 2. 返回项目根目录启动所有服务
cd /workspace
docker-compose up -d

# 3. 验证服务
curl http://localhost:8002/health

# 4. 运行测试
cd backend/ai-service
./test_docker.sh
```

## 📦 包含的服务

### AI Service 相关
- **ai-service**: FastAPI 服务 (端口 8002)
- **ai-worker**: Celery 异步任务处理器
- **redis**: Redis 数据库 (端口 6379) - 与 video-service 共享

### 相关服务
- **api-gateway**: API 网关 (端口 8001)
- **video-service**: 视频合成服务 (端口 8003)
- **video-worker**: 视频合成 Worker
- **frontend**: 前端界面 (端口 3000)

## 🔧 核心配置

`.env` 文件必填配置：

```env
# ⚠️ 必填: 七牛 AI Token API Key
QINIU_API_KEY=your-qiniu-ai-token-api-key

# 以下配置使用默认值即可（Docker 环境）
REDIS_URL=redis://redis:6379/0
VIDEO_SERVICE_URL=http://video-service:8003
LOCAL_STORAGE_DIR=/tmp/tfboys
```

## ✅ 验证服务

### 1. 检查容器状态
```bash
docker-compose ps
```

所有容器应显示 `Up` 或 `Up (healthy)` 状态。

### 2. 健康检查
```bash
# AI Service
curl http://localhost:8002/health

# Video Service
curl http://localhost:8003/health

# API Gateway
curl http://localhost:8001/health
```

### 3. 查看日志
```bash
# 实时查看 AI Service 日志
docker-compose logs -f ai-service ai-worker
```

### 4. 查看 API 文档
浏览器访问：
- AI Service: http://localhost:8002/docs
- Video Service: http://localhost:8003/docs
- API Gateway: http://localhost:8001/docs

## 🧪 快速测试

### 方式 1: 使用测试脚本

```bash
cd backend/ai-service
./test_docker.sh
```

### 方式 2: 手动测试

创建测试任务：
```bash
curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_001",
    "novel_text": "小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。"
  }'
```

查询任务状态：
```bash
curl http://localhost:8002/internal/tasks/test_001
```

持续监控任务：
```bash
watch -n 2 'curl -s http://localhost:8002/internal/tasks/test_001 | jq ".status"'
```

### 方式 3: 通过 API Gateway（完整链路）

```bash
curl -X POST "http://localhost:8001/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_gateway_001",
    "novel_text": "小猫在树上玩耍，小狗在地上跑来跑去。"
  }'

# 查询任务
curl http://localhost:8001/tasks/test_gateway_001
```

## 🎬 完整工作流示例

```bash
# 1. 创建任务
TASK_ID="demo_$(date +%s)"
curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d "{
    \"task_id\": \"$TASK_ID\",
    \"novel_text\": \"小明是个活泼的男孩。他喜欢运动和读书。今天天气很好，他决定去公园玩。\"
  }"

# 2. 持续监控
while true; do
  STATUS=$(curl -s http://localhost:8002/internal/tasks/$TASK_ID | jq -r '.status')
  echo "[$(date '+%H:%M:%S')] Task $TASK_ID: $STATUS"
  
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    break
  fi
  
  sleep 3
done

# 3. 查看最终结果
curl http://localhost:8002/internal/tasks/$TASK_ID | jq '.'
```

## 🛠️ 常用命令

### 启动/停止服务

```bash
# 启动所有服务
docker-compose up -d

# 仅启动 AI Service 相关
docker-compose up -d redis ai-service ai-worker

# 停止所有服务
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除容器 + 数据卷
docker-compose down -v
```

### 查看日志

```bash
# 所有服务日志
docker-compose logs -f

# AI Service 日志
docker-compose logs -f ai-service

# AI Worker 日志
docker-compose logs -f ai-worker

# 最近 50 行
docker-compose logs --tail=50 ai-service
```

### 重启服务

```bash
# 重启 AI Service
docker-compose restart ai-service ai-worker

# 重启所有服务
docker-compose restart
```

### 重新构建镜像

```bash
# 代码更新后重新构建
docker-compose build ai-service
docker-compose up -d ai-service ai-worker

# 强制重新构建（清除缓存）
docker-compose build --no-cache ai-service
docker-compose up -d ai-service ai-worker
```

### 进入容器调试

```bash
# 进入 ai-service 容器
docker-compose exec ai-service bash

# 进入 ai-worker 容器
docker-compose exec ai-worker bash

# 进入 Redis
docker-compose exec redis redis-cli
```

### 查看 Celery 状态

```bash
# 查看活跃任务
docker-compose exec ai-worker celery -A app.workers.celery_app inspect active

# 查看已注册任务
docker-compose exec ai-worker celery -A app.workers.celery_app inspect registered

# 查看 Worker 统计
docker-compose exec ai-worker celery -A app.workers.celery_app inspect stats
```

## 🐛 常见问题

### 问题 1: 容器无法启动

**检查方法**：
```bash
docker-compose logs ai-service
```

**常见原因**：
- .env 文件未配置或格式错误
- QINIU_API_KEY 未设置
- 端口被占用（8002）

**解决方案**：
```bash
# 检查端口占用
lsof -i :8002

# 检查配置文件
cat backend/ai-service/.env

# 重新配置
cd backend/ai-service
cp .env.example .env
nano .env
```

### 问题 2: 任务一直 pending

**检查方法**：
```bash
docker-compose logs ai-worker
docker-compose ps ai-worker
```

**解决方案**：
```bash
# 确认 Worker 运行
docker-compose ps ai-worker

# 重启 Worker
docker-compose restart ai-worker

# 检查 Redis 连接
docker-compose exec redis redis-cli ping
```

### 问题 3: API Key 错误

**症状**：任务失败，日志显示 401 或 API 错误

**解决方案**：
```bash
# 检查环境变量
docker-compose exec ai-service env | grep QINIU

# 更新配置
nano backend/ai-service/.env

# 重启服务
docker-compose restart ai-service ai-worker
```

### 问题 4: 存储目录权限问题

**症状**：图像或音频生成失败

**解决方案**：
```bash
# 检查目录
docker-compose exec ai-service ls -la /tmp/tfboys

# 测试写入
docker-compose exec ai-service touch /tmp/tfboys/test.txt

# 修复权限
docker-compose exec ai-service chmod 777 /tmp/tfboys
```

## 📊 监控和调试

### 实时监控任务状态

创建监控脚本 `monitor.sh`：
```bash
#!/bin/bash
TASK_ID=$1

while true; do
  RESPONSE=$(curl -s http://localhost:8002/internal/tasks/$TASK_ID)
  STATUS=$(echo $RESPONSE | jq -r '.status')
  PROGRESS=$(echo $RESPONSE | jq -r '.progress.percentage // 0')
  
  echo "[$(date '+%H:%M:%S')] Status: $STATUS, Progress: $PROGRESS%"
  
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    echo "Task finished!"
    echo $RESPONSE | jq '.'
    break
  fi
  
  sleep 2
done
```

使用：
```bash
chmod +x monitor.sh
./monitor.sh test_001
```

### 查看 Redis 数据

```bash
# 连接到 Redis
docker-compose exec redis redis-cli

# 查看所有任务
KEYS task:*

# 查看特定任务
GET task:test_001

# 查看 Celery 队列
KEYS celery*

# 退出
exit
```

### 资源监控

```bash
# 查看容器资源使用
docker stats tfboys-ai-service tfboys-ai-worker

# 查看存储使用
docker-compose exec ai-service du -sh /tmp/tfboys/*
```

## 🔄 与现有 Video Service 集成

### 场景: Video Service 已经在运行

如果你已经部署了 video-service，现在要添加 ai-service：

```bash
# 1. 配置 AI Service
cd backend/ai-service
cp .env.example .env
nano .env  # 设置 QINIU_API_KEY

# 2. 启动 AI Service（不影响 video-service）
cd /workspace
docker-compose up -d ai-service ai-worker

# 3. 验证集成
curl http://localhost:8002/health
curl http://localhost:8003/health

# 4. 测试完整链路
curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "integration_test",
    "novel_text": "测试 AI Service 和 Video Service 集成。"
  }'
```

### 共享资源

AI Service 和 Video Service 自动共享：
- **Redis**: 同一个 Redis 实例
- **存储**: 同一个 Docker volume (`tfboys-storage`)
- **网络**: 同一个 Docker network (`tfboys-network`)

无需额外配置！

## 📈 性能优化

### 增加 Worker 并发

编辑 `docker-compose.yml`:
```yaml
ai-worker:
  command: celery -A app.workers.celery_app worker --loglevel=info --concurrency=4
```

然后重启：
```bash
docker-compose up -d ai-worker
```

### 限制资源使用

编辑 `docker-compose.yml`:
```yaml
ai-service:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 2G
```

## 📖 详细文档

- **完整部署文档**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **端到端测试**: [E2E_TESTING.md](./E2E_TESTING.md)
- **快速开始**: [QUICKSTART.md](./QUICKSTART.md)
- **开发指南**: [README.md](./README.md)

## 🆘 获取帮助

问题排查步骤：
1. 查看容器状态：`docker-compose ps`
2. 查看日志：`docker-compose logs -f ai-service ai-worker`
3. 检查健康：`curl http://localhost:8002/health`
4. 检查配置：`cat backend/ai-service/.env`
5. 参考 [DEPLOYMENT.md](./DEPLOYMENT.md) 详细故障排查指南

---

**快速链接**：
- API 文档: http://localhost:8002/docs
- 健康检查: http://localhost:8002/health
- Redis: localhost:6379

**最后更新**: 2025-10-26
