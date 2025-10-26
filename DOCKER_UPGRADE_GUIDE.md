# Docker 测试环境升级指南

本文档提供从现有 Video Service Docker 环境升级到包含 AI Service 的完整系统的详细步骤。

## 📋 升级概述

### 升级前
- ✅ Video Service (端口 8003)
- ✅ Video Worker (Celery)
- ✅ Redis (端口 6379)

### 升级后
- ✅ Video Service (端口 8003)
- ✅ Video Worker (Celery)
- ✅ Redis (端口 6379) - 共享
- ✨ **AI Service (端口 8002)** - 新增
- ✨ **AI Worker (Celery)** - 新增
- ✨ **API Gateway (端口 8001)** - 新增
- ✨ **Frontend (端口 3000)** - 新增（可选）

## 🎯 升级目标

1. 保留现有 Video Service 的数据和配置
2. 添加 AI Service 及其依赖服务
3. 确保 AI Service 和 Video Service 正确集成
4. 共享 Redis 和存储资源
5. 最小化停机时间

## ⚠️ 升级前准备

### 1. 备份现有数据

```bash
# 进入项目根目录
cd /workspace

# 备份 Redis 数据
docker exec tfboys-redis redis-cli BGSAVE
docker cp tfboys-redis:/data/dump.rdb ./backup/redis-$(date +%Y%m%d-%H%M%S).rdb

# 备份 Video Service 环境配置
cp backend/video-service/.env backend/video-service/.env.backup-$(date +%Y%m%d-%H%M%S)

# 备份生成的文件（如果有）
mkdir -p ./backup/tfboys-$(date +%Y%m%d-%H%M%S)
docker cp tfboys-video-service:/tmp/tfboys ./backup/tfboys-$(date +%Y%m%d-%H%M%S)/ || true
```

### 2. 检查当前环境

```bash
# 查看当前运行的容器
docker ps

# 查看当前 docker-compose 配置
docker-compose config

# 检查端口占用
lsof -i :8001  # API Gateway
lsof -i :8002  # AI Service
lsof -i :8003  # Video Service (已使用)
lsof -i :3000  # Frontend
lsof -i :6379  # Redis (已使用)
```

### 3. 记录当前配置

```bash
# 导出当前容器列表
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" > ./backup/containers-before-$(date +%Y%m%d).txt

# 导出当前 volume 列表
docker volume ls > ./backup/volumes-before-$(date +%Y%m%d).txt
```

## 🚀 升级步骤

### 步骤 1: 准备 AI Service 配置

```bash
# 创建 AI Service 环境配置
cd backend/ai-service
cp .env.example .env

# 编辑配置文件
nano .env
```

**必须配置的内容**：
```env
# ⚠️ 必填: 七牛 AI Token API Key
QINIU_API_KEY=your-qiniu-ai-token-api-key

# 以下使用默认值（Docker 环境）
REDIS_URL=redis://redis:6379/0
VIDEO_SERVICE_URL=http://video-service:8003
LOCAL_STORAGE_DIR=/tmp/tfboys
```

**获取七牛 API Key**: https://portal.qiniu.com/kodo/ak-sk

### 步骤 2: 检查 docker-compose.yml 配置

项目根目录的 `docker-compose.yml` 已包含完整配置，无需修改。

验证配置：
```bash
cd /workspace

# 检查配置是否正确
docker-compose config

# 查看将要启动的服务
docker-compose config --services
```

预期输出应包含：
```
redis
api-gateway
ai-service
ai-worker
video-service
video-worker
frontend
```

### 步骤 3: 更新 Video Service 配置（可选）

如果需要让 Video Service 回调 AI Service，确保 `.env` 包含：

```bash
cd backend/video-service
nano .env
```

添加或更新：
```env
AI_SERVICE_CALLBACK_URL=http://ai-service:8002/callbacks/video-completed
```

### 步骤 4: 停止现有服务

```bash
cd /workspace

# 停止所有容器（不删除数据）
docker-compose stop

# 或者只停止 video-service 和 worker
docker-compose stop video-service video-worker
```

**注意**: 
- 使用 `stop` 而不是 `down`，保留现有数据
- Redis 容器可以继续运行，也可以停止

### 步骤 5: 启动升级后的完整系统

```bash
cd /workspace

# 启动所有服务（包括新增的 AI Service）
docker-compose up -d

# 查看启动日志
docker-compose logs -f
```

**预期输出**：
- 所有容器状态为 `Up` 或 `Up (healthy)`
- 没有错误日志

### 步骤 6: 验证服务状态

```bash
# 检查所有容器
docker-compose ps

# 预期看到:
# - tfboys-redis          Up (healthy)
# - tfboys-api-gateway    Up
# - tfboys-ai-service     Up (healthy)
# - tfboys-ai-worker      Up
# - tfboys-video-service  Up (healthy)
# - tfboys-video-worker   Up
# - tfboys-frontend       Up
```

### 步骤 7: 健康检查

```bash
# Redis
docker exec tfboys-redis redis-cli ping
# 预期: PONG

# Video Service
curl http://localhost:8003/health
# 预期: {"status": "healthy"}

# AI Service（新增）
curl http://localhost:8002/health
# 预期: {"status": "healthy", "service": "ai-service"}

# API Gateway（新增）
curl http://localhost:8001/health
# 预期: {"status": "healthy"}
```

### 步骤 8: 验证服务集成

```bash
# 测试 AI Service 调用 Video Service
curl -X POST "http://localhost:8002/internal/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "upgrade_test_001",
    "novel_text": "这是升级后的集成测试。小明和小红一起去公园玩。"
  }'

# 监控任务状态
watch -n 2 'curl -s http://localhost:8002/internal/tasks/upgrade_test_001 | jq ".status"'
```

预期流程：
1. AI Service 接收任务 → `pending`
2. AI Worker 开始处理 → `analyzing`
3. 生成图像 → `generating_images`
4. 生成音频 → `generating_audio`
5. 调用 Video Service → `synthesizing_video`
6. 视频完成 → `completed`

### 步骤 9: 验证数据持久化

```bash
# 检查 Redis 数据
docker exec tfboys-redis redis-cli KEYS "task:*"

# 检查存储卷
docker volume ls | grep tfboys

# 检查存储目录内容
docker exec tfboys-ai-service ls -la /tmp/tfboys
docker exec tfboys-video-service ls -la /tmp/tfboys

# 两个服务应该看到相同的文件（共享存储）
```

## 🧪 完整测试

运行 AI Service 测试脚本：

```bash
cd backend/ai-service
./test_docker.sh
```

测试脚本会验证：
- ✅ Docker 服务状态
- ✅ 健康检查
- ✅ Celery Worker 状态
- ✅ 存储目录权限
- ✅ 创建测试任务
- ✅ 监控任务进度
- ✅ 验证最终结果

## 📊 升级验证清单

完成以下所有检查，确认升级成功：

- [ ] 所有容器运行正常 (`docker-compose ps`)
- [ ] Redis 健康检查通过
- [ ] Video Service 健康检查通过
- [ ] AI Service 健康检查通过（新）
- [ ] API Gateway 健康检查通过（新）
- [ ] AI Worker 已注册任务
- [ ] Video Worker 已注册任务
- [ ] 存储卷正确共享
- [ ] AI Service 可以调用 Video Service
- [ ] 测试任务成功完成
- [ ] 无错误日志

## 🐛 常见升级问题

### 问题 1: 端口冲突

**症状**：容器启动失败，提示端口被占用

**解决方案**：
```bash
# 检查端口占用
lsof -i :8001
lsof -i :8002

# 停止占用端口的进程，或修改 docker-compose.yml 端口映射
# 例如，将 8002 改为 8012:
# ports:
#   - "8012:8002"
```

### 问题 2: AI Service 无法连接 Redis

**症状**：AI Worker 日志显示 Redis 连接错误

**解决方案**：
```bash
# 检查 Redis 容器名称
docker ps | grep redis

# 确认 docker-compose.yml 中 Redis 服务名为 "redis"
# 确认 AI Service .env 文件中:
# REDIS_URL=redis://redis:6379/0

# 重启服务
docker-compose restart redis ai-service ai-worker
```

### 问题 3: AI Service 找不到 shared 模块

**症状**：日志显示 "No module named 'shared'"

**解决方案**：
```bash
# 检查 docker-compose.yml 中 volume 配置
docker-compose config | grep -A 10 ai-service

# 应该包含:
# volumes:
#   - ./shared:/app/shared:ro

# 如果缺失，添加后重新启动
docker-compose up -d ai-service ai-worker
```

### 问题 4: Video Service 和 AI Service 数据不同步

**症状**：AI Service 生成的文件，Video Service 看不到

**解决方案**：
```bash
# 确认使用同一个 volume
docker volume ls | grep tfboys-storage

# 检查 docker-compose.yml 中两个服务都挂载了:
# volumes:
#   - tfboys-storage:/tmp/tfboys

# 验证共享
docker exec tfboys-ai-service touch /tmp/tfboys/test.txt
docker exec tfboys-video-service ls -la /tmp/tfboys/test.txt
# 应该能看到文件

# 清理测试文件
docker exec tfboys-ai-service rm /tmp/tfboys/test.txt
```

### 问题 5: 七牛 API Key 未配置

**症状**：任务失败，日志显示 401 或 API 错误

**解决方案**：
```bash
# 检查环境变量
docker exec tfboys-ai-service env | grep QINIU

# 更新配置
nano backend/ai-service/.env
# 设置: QINIU_API_KEY=your-real-key

# 重启服务使配置生效
docker-compose restart ai-service ai-worker
```

### 问题 6: 旧任务数据冲突

**症状**：升级后旧任务状态异常

**解决方案**：
```bash
# 清理 Redis 中的旧任务数据（谨慎操作）
docker exec tfboys-redis redis-cli --scan --pattern "task:*" | xargs docker exec -i tfboys-redis redis-cli DEL

# 或者只清理特定任务
docker exec tfboys-redis redis-cli DEL task:old_task_id
```

## 🔄 回滚步骤

如果升级失败，需要回滚到原始状态：

### 回滚步骤

```bash
# 1. 停止所有服务
docker-compose down

# 2. 恢复 Video Service 配置
cp backend/video-service/.env.backup-YYYYMMDD backend/video-service/.env

# 3. 恢复 Redis 数据（如果需要）
docker cp ./backup/redis-YYYYMMDD.rdb tfboys-redis:/data/dump.rdb
docker exec tfboys-redis redis-cli SHUTDOWN SAVE
docker-compose start redis

# 4. 仅启动原有服务
docker-compose up -d redis video-service video-worker

# 5. 验证
curl http://localhost:8003/health
docker-compose ps
```

## 📈 升级后优化建议

### 1. 调整资源限制

编辑 `docker-compose.yml`，为每个服务设置资源限制：

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

### 2. 增加 Worker 并发数

```yaml
ai-worker:
  command: celery -A app.workers.celery_app worker --loglevel=info --concurrency=4

video-worker:
  command: celery -A app.workers.celery_app worker --loglevel=info --concurrency=4
```

### 3. 配置日志管理

```yaml
ai-service:
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
```

### 4. 启用自动重启

已在 `docker-compose.yml` 中配置：
```yaml
restart: unless-stopped
```

### 5. 添加监控（可选）

添加 Flower 监控 Celery：
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

## 📚 升级后的系统架构

```
                    ┌──────────────┐
                    │   Frontend   │ :3000
                    └──────┬───────┘
                           │
                           v
                    ┌──────────────┐
                    │ API Gateway  │ :8001
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              v                         v
       ┌─────────────┐          ┌──────────────┐
       │ AI Service  │ :8002    │Video Service │ :8003
       ├─────────────┤          ├──────────────┤
       │  AI Worker  │◄────────►│Video Worker  │
       └──────┬──────┘          └──────┬───────┘
              │                        │
              └───────────┬────────────┘
                          │
                          v
                   ┌─────────────┐
                   │    Redis    │ :6379
                   └─────────────┘
                          │
                          v
                   ┌─────────────┐
                   │   Storage   │ /tmp/tfboys
                   │  (共享卷)   │
                   └─────────────┘
```

## 🎯 验证升级成功的标志

✅ **所有检查通过后，升级成功：**

1. ✅ 7 个容器全部运行（或至少 5 个核心容器）
2. ✅ 所有健康检查通过
3. ✅ AI Service 和 Video Service 可以相互通信
4. ✅ 测试任务从创建到完成全流程正常
5. ✅ 共享存储正常工作
6. ✅ Redis 数据正常访问
7. ✅ 无错误日志

## 📖 相关文档

- [AI Service 部署文档](./backend/ai-service/DEPLOYMENT.md)
- [AI Service Docker 快速指南](./backend/ai-service/README.Docker.md)
- [Video Service 部署文档](./backend/video-service/DEPLOYMENT.md)
- [项目开发指南](./CLAUDE.md)

## 🆘 获取帮助

如果升级过程中遇到问题：

1. 查看日志：`docker-compose logs -f`
2. 检查容器状态：`docker-compose ps`
3. 运行测试：`cd backend/ai-service && ./test_docker.sh`
4. 参考故障排查章节
5. 提交 Issue 到项目仓库

---

**最后更新**: 2025-10-26
**维护者**: TFBoys Team
