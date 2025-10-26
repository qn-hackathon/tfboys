# AI Service Docker 部署指南

本文档提供 ai-service 完整的 Docker 测试环境部署步骤。

## 📋 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间
- 七牛 AI Token API Key（必需）

## 🚀 快速开始

### 步骤 1: 准备配置文件

```bash
cd backend/ai-service
cp .env.example .env
```

编辑 `.env` 文件，**必须**填入七牛 API Key：

```bash
nano .env
```

**关键配置**：
```env
# ⚠️ 必填: 七牛 AI Token API Key
QINIU_API_KEY=your-qiniu-ai-token-api-key

# 其他配置（Docker 环境下使用默认值即可）
REDIS_URL=redis://redis:6379/0
VIDEO_SERVICE_URL=http://video-service:8003
LOCAL_STORAGE_DIR=/tmp/tfboys
```

**⚠️ 重要**: 必须将 `your-qiniu-ai-token-api-key` 替换为真实的七牛 API Key，否则 AI 功能无法正常工作。

### 步骤 2: 启动所有服务（项目根目录）

如果 video-service 已经启动，需要先停止：

```bash
# 返回项目根目录
cd /workspace

# 停止现有服务（如果有）
docker-compose down

# 重新启动所有服务（包括 ai-service 和 video-service）
docker-compose up -d
```

这将启动以下服务：
1. **redis**: Redis 数据库（端口 6379）
2. **api-gateway**: API 网关（端口 8001）
3. **ai-service**: AI Service API（端口 8002）
4. **ai-worker**: AI Service Celery Worker
5. **video-service**: Video Service API（端口 8003）
6. **video-worker**: Video Service Celery Worker
7. **frontend**: 前端服务（端口 3000）

### 步骤 3: 验证服务状态

```bash
docker-compose ps
```

预期输出：
```
NAME                     COMMAND                  SERVICE         STATUS
tfboys-ai-service        "uvicorn app.main:ap…"   ai-service      Up (healthy)
tfboys-ai-worker         "celery -A app.worke…"   ai-worker       Up
tfboys-api-gateway       "uvicorn app.main:ap…"   api-gateway     Up
tfboys-redis             "docker-entrypoint.s…"   redis           Up (healthy)
tfboys-video-service     "uvicorn app.main:ap…"   video-service   Up (healthy)
tfboys-video-worker      "celery -A app.worke…"   video-worker    Up
tfboys-frontend          "/docker-entrypoint.…"   frontend        Up
```

检查 AI Service 健康状态：

```bash
curl http://localhost:8002/health
```

预期响应：
```json
{"status": "healthy", "service": "ai-service"}
```

## 🔍 详细操作命令

### 仅启动 AI Service 相关容器

如果只想测试 AI Service（不启动 video-service 和 frontend）：

```bash
docker-compose up -d redis ai-service ai-worker
```

### 查看日志

查看所有服务日志：
```bash
docker-compose logs -f
```

查看 AI Service 相关日志：
```bash
# AI Service API 日志
docker-compose logs -f ai-service

# AI Worker 日志
docker-compose logs -f ai-worker

# Redis 日志
docker-compose logs -f redis
```

### 进入容器

进入 ai-service 容器：
```bash
docker-compose exec ai-service bash
```

进入 ai-worker 容器：
```bash
docker-compose exec ai-worker bash
```

进入 Redis 容器：
```bash
docker-compose exec redis redis-cli
```

### 重启服务

重启所有服务：
```bash
docker-compose restart
```

重启 AI Service：
```bash
docker-compose restart ai-service ai-worker
```

### 停止服务

停止但不删除容器：
```bash
docker-compose stop
```

停止并删除容器：
```bash
docker-compose down
```

停止并删除容器及数据卷：
```bash
docker-compose down -v
```

### 重新构建镜像

当代码更新后：
```bash
# 重新构建 ai-service 镜像
docker-compose build ai-service

# 重新启动
docker-compose up -d ai-service ai-worker
```

强制重新构建（清除缓存）：
```bash
docker-compose build --no-cache ai-service
docker-compose up -d ai-service ai-worker
```

### 查看资源占用

查看容器资源使用情况：
```bash
docker stats
```

查看 AI Service 特定容器：
```bash
docker stats tfboys-ai-service tfboys-ai-worker
```

## 🧪 测试方法

### 1. 健康检查测试

```bash
curl http://localhost:8002/health
```

预期响应：
```json
{"status": "healthy", "service": "ai-service"}
```

### 2. API 文档测试

在浏览器中访问：
```
http://localhost:8002/docs
```

### 3. Redis 连接测试

```bash
docker-compose exec redis redis-cli ping
```

预期输出：`PONG`

### 4. Celery Worker 测试

查看 Celery Worker 状态：
```bash
docker-compose exec ai-worker celery -A app.workers.celery_app inspect active
```

查看已注册的任务：
```bash
docker-compose exec ai-worker celery -A app.workers.celery_app inspect registered
```

预期输出应包含：
```json
{
  "celery@xxx": {
    "app.workers.tasks.process_novel_task": {...}
  }
}
```

### 5. 存储目录测试

验证存储目录权限：
```bash
docker-compose exec ai-service ls -la /tmp/tfboys
docker-compose exec ai-service touch /tmp/tfboys/test.txt
```

### 6. 完整工作流测试

使用内部 API 创建任务：

```bash
curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_docker_001",
    "novel_text": "小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。"
  }'
```

预期响应：
```json
{
  "task_id": "test_docker_001",
  "status": "pending"
}
```

查询任务状态：
```bash
curl http://localhost:8002/internal/tasks/test_docker_001
```

### 7. 通过 API Gateway 测试（完整链路）

```bash
curl -X POST "http://localhost:8001/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_gateway_001",
    "novel_text": "小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。"
  }'
```

查询任务：
```bash
curl http://localhost:8001/tasks/test_gateway_001
```

## 📊 测试示例

### 示例 1: 短文本处理测试

```bash
cat > test_short.json <<EOF
{
  "task_id": "test_short_001",
  "novel_text": "小猫在树上玩耍。"
}
EOF

curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d @test_short.json
```

### 示例 2: 多场景文本测试

```bash
cat > test_multi.json <<EOF
{
  "task_id": "test_multi_001",
  "novel_text": "小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。老师开始讲课，小明认真听讲。"
}
EOF

curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d @test_multi.json
```

### 示例 3: 监控任务进度

创建一个脚本持续监控任务状态：

```bash
cat > monitor_task.sh <<'EOF'
#!/bin/bash
TASK_ID=$1

if [ -z "$TASK_ID" ]; then
  echo "Usage: $0 <task_id>"
  exit 1
fi

echo "Monitoring task: $TASK_ID"
while true; do
  STATUS=$(curl -s http://localhost:8002/internal/tasks/$TASK_ID | jq -r '.status')
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Status: $STATUS"
  
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    echo "Task finished with status: $STATUS"
    curl -s http://localhost:8002/internal/tasks/$TASK_ID | jq '.'
    break
  fi
  
  sleep 3
done
EOF

chmod +x monitor_task.sh

# 使用方法
./monitor_task.sh test_multi_001
```

## 🐛 故障排查

### 问题 1: ai-service 容器无法启动

**症状**：`docker-compose up -d` 后 ai-service 状态为 Exit

**解决方案**：
```bash
# 查看详细错误日志
docker-compose logs ai-service

# 常见原因：
# 1. .env 文件缺失或格式错误
# 2. QINIU_API_KEY 未设置
# 3. 端口 8002 被占用
```

检查端口占用：
```bash
lsof -i :8002
```

### 问题 2: ai-worker 无法连接到 Redis

**症状**：ai-worker 日志显示 Redis 连接错误

**解决方案**：
```bash
# 检查 Redis 是否健康
docker-compose exec redis redis-cli ping

# 如果无响应，重启 Redis
docker-compose restart redis

# 等待 Redis 健康后重启 worker
docker-compose restart ai-worker
```

### 问题 3: Celery Worker 报错 "wrong number of arguments for 'ping' command"

**症状**：ai-worker 日志显示 Redis 命令错误

**原因**：Redis 版本不兼容

**解决方案**：
```bash
# 检查 requirements.txt 中的 redis 版本
cat backend/ai-service/requirements.txt | grep redis

# 应该是 redis==4.6.0
# 如果不是，更新 requirements.txt 后重新构建镜像
docker-compose build --no-cache ai-service
docker-compose up -d ai-service ai-worker
```

### 问题 4: 七牛 API 调用失败

**症状**：任务状态变为 failed，日志显示 API 错误

**解决方案**：
```bash
# 检查环境变量
docker-compose exec ai-service env | grep QINIU

# 确认 API Key 正确
# 重新编辑 .env 文件，更新 QINIU_API_KEY
nano backend/ai-service/.env

# 重启服务使配置生效
docker-compose restart ai-service ai-worker
```

### 问题 5: 任务一直处于 pending 状态

**可能原因**：
- Celery Worker 未启动
- Redis 队列问题

**解决方案**：
```bash
# 检查 Celery Worker 是否运行
docker-compose ps ai-worker

# 查看 Worker 日志
docker-compose logs -f ai-worker

# 检查 Redis 队列
docker-compose exec redis redis-cli
> KEYS celery*
> exit

# 重启 Worker
docker-compose restart ai-worker
```

### 问题 6: 本地存储访问失败

**症状**：图像或音频生成失败，日志显示文件写入错误

**解决方案**：
```bash
# 检查存储目录权限
docker-compose exec ai-service ls -la /tmp/tfboys

# 测试写入权限
docker-compose exec ai-service touch /tmp/tfboys/test.txt
docker-compose exec ai-service rm /tmp/tfboys/test.txt

# 如果权限有问题，重新创建目录
docker-compose exec ai-service mkdir -p /tmp/tfboys
docker-compose exec ai-service chmod 777 /tmp/tfboys
```

### 问题 7: 无法访问 shared 模块

**症状**：日志显示 "No module named 'shared'"

**解决方案**：
```bash
# 检查 docker-compose.yml 中的 volume 配置
grep -A 5 "ai-service:" docker-compose.yml | grep shared

# 应该包含:
# - ./shared:/app/shared:ro

# 重新启动服务
docker-compose restart ai-service ai-worker
```

## 🔄 与 Video Service 集成

### 共享组件

AI Service 和 Video Service 共享以下组件：
1. **Redis**: 统一使用 `tfboys-redis` 容器
2. **存储卷**: 统一使用 `tfboys-storage` volume
3. **网络**: 统一使用 `tfboys-network` 网络
4. **Shared 模块**: 通过 volume 挂载共享

### 升级已有 Video Service 环境

如果之前只部署了 video-service，现在需要添加 ai-service：

#### 步骤 1: 备份现有数据（可选）

```bash
# 导出 Redis 数据
docker-compose exec redis redis-cli BGSAVE

# 备份生成的视频文件
docker cp tfboys-video-service:/tmp/tfboys /backup/tfboys-$(date +%Y%m%d)
```

#### 步骤 2: 更新 docker-compose.yml

已有的 `docker-compose.yml` 已包含 ai-service 配置，无需修改。

#### 步骤 3: 配置 AI Service 环境变量

```bash
cd backend/ai-service
cp .env.example .env
nano .env
# 设置 QINIU_API_KEY
```

#### 步骤 4: 启动 AI Service

```bash
# 返回项目根目录
cd /workspace

# 构建并启动 ai-service
docker-compose up -d ai-service ai-worker
```

#### 步骤 5: 验证集成

```bash
# 检查所有服务状态
docker-compose ps

# 测试 AI Service → Video Service 集成
# 创建一个完整的视频生成任务
curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "integration_test_001",
    "novel_text": "小明和小红一起去公园玩。"
  }'

# 监控任务状态
watch -n 2 'curl -s http://localhost:8002/internal/tasks/integration_test_001 | jq ".status"'
```

#### 步骤 6: 验证回调机制

AI Service 完成处理后会调用 Video Service，Video Service 完成后会回调 AI Service。

检查回调配置：
```bash
# Video Service 环境变量应包含
docker-compose exec video-service env | grep AI_SERVICE_CALLBACK_URL
# 应输出: AI_SERVICE_CALLBACK_URL=http://ai-service:8002/callbacks/video-completed

# AI Service 环境变量应包含
docker-compose exec ai-service env | grep VIDEO_SERVICE_URL
# 应输出: VIDEO_SERVICE_URL=http://video-service:8003
```

### 完整系统架构

```
┌─────────────┐
│  Frontend   │ :3000
└──────┬──────┘
       │
       v
┌─────────────┐
│ API Gateway │ :8001
└──────┬──────┘
       │
       v
┌─────────────┐      ┌──────────────┐
│ AI Service  │ :8002│ Video Service│ :8003
├─────────────┤      ├──────────────┤
│ AI Worker   │◄────►│ Video Worker │
└──────┬──────┘      └──────┬───────┘
       │                    │
       └────────┬───────────┘
                │
                v
         ┌─────────────┐
         │    Redis    │ :6379
         └─────────────┘
```

## 📈 性能优化建议

### 1. 增加 Celery Worker 并发数

编辑 `docker-compose.yml`：
```yaml
ai-worker:
  command: celery -A app.workers.celery_app worker --loglevel=info --concurrency=4
```

### 2. 限制资源使用

在 `docker-compose.yml` 中添加资源限制：
```yaml
ai-service:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 2G
      reservations:
        cpus: '1.0'
        memory: 1G
```

### 3. 使用 SSD 存储

将本地存储目录映射到 SSD：
```yaml
volumes:
  tfboys-storage:
    driver: local
    driver_opts:
      type: none
      device: /path/to/ssd/tfboys
      o: bind
```

### 4. Redis 持久化优化

编辑 `docker-compose.yml` 中的 Redis 配置：
```yaml
redis:
  command: redis-server --appendonly yes --save 60 1000
```

## 🔒 安全建议

1. **不要在生产环境中使用默认配置**
2. **使用环境变量管理敏感信息**（特别是 QINIU_API_KEY）
3. **定期更新 Docker 镜像**
4. **限制容器网络访问**
5. **不要将 .env 文件提交到版本控制**
6. **使用 Docker secrets 管理密钥**（生产环境）

## 📚 监控和日志

### 查看实时日志

```bash
# 所有服务
docker-compose logs -f

# AI Service + Worker
docker-compose logs -f ai-service ai-worker

# 最近 100 行
docker-compose logs --tail=100 ai-service
```

### 日志持久化

在 `docker-compose.yml` 中配置日志驱动：
```yaml
ai-service:
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
```

### 监控 Celery 任务

可选：部署 Flower 监控 Celery：
```yaml
flower:
  image: mher/flower
  command: celery --broker=redis://redis:6379/0 flower --port=5555
  ports:
    - "5555:5555"
  depends_on:
    - redis
  networks:
    - tfboys-network
```

访问 http://localhost:5555 查看 Celery 任务状态。

## 📊 验证清单

完成以下所有检查，确认部署成功：

- [ ] Docker 和 Docker Compose 已安装
- [ ] `.env` 文件已配置，QINIU_API_KEY 已设置
- [ ] 所有容器启动成功 (`docker-compose ps` 全部 Up)
- [ ] Redis 健康检查通过 (`curl http://localhost:6379` 或 `redis-cli ping`)
- [ ] AI Service 健康检查通过 (`curl http://localhost:8002/health`)
- [ ] Video Service 健康检查通过 (`curl http://localhost:8003/health`)
- [ ] API Gateway 健康检查通过 (`curl http://localhost:8001/health`)
- [ ] Celery Worker 已注册任务 (`celery inspect registered`)
- [ ] 存储目录可写 (`touch /tmp/tfboys/test.txt`)
- [ ] 测试任务创建成功
- [ ] 测试任务最终状态为 `completed`
- [ ] 无错误日志

## 🆘 获取帮助

如遇到问题，请：
1. 查看容器日志：`docker-compose logs -f ai-service ai-worker`
2. 检查环境配置：`backend/ai-service/.env`
3. 查看 API 文档：http://localhost:8002/docs
4. 查看健康检查：`curl http://localhost:8002/health`
5. 提交 Issue 到项目仓库

## 📚 相关文档

- [快速启动指南](./QUICKSTART.md)
- [端到端测试指南](./E2E_TESTING.md)
- [Video Service 部署指南](../video-service/DEPLOYMENT.md)
- [项目开发指南](/CLAUDE.md)

---

**最后更新**: 2025-10-26
**维护者**: TFBoys Team
