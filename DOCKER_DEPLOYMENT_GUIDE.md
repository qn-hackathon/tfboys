# TFBoys AI Service Docker 测试环境部署指南

本文档提供 AI Service 在 Docker 环境下的完整部署流程，包括与 Video Service 的集成配置。

## 📋 目录

- [环境要求](#环境要求)
- [架构说明](#架构说明)
- [快速开始](#快速开始)
- [详细部署步骤](#详细部署步骤)
- [测试验证](#测试验证)
- [常见问题](#常见问题)
- [运维管理](#运维管理)

---

## 环境要求

### 硬件要求
- **CPU**: 4 核心以上
- **内存**: 8GB 以上 (推荐 16GB)
- **磁盘**: 至少 20GB 可用空间

### 软件要求
- **Docker**: 20.10.0 或更高版本
- **Docker Compose**: 2.0.0 或更高版本
- **操作系统**: Linux (推荐 Ubuntu 20.04+) / macOS / Windows with WSL2

### 验证安装

```bash
# 检查 Docker 版本
docker --version
# 预期输出: Docker version 20.10.x 或更高

# 检查 Docker Compose 版本
docker compose version
# 预期输出: Docker Compose version v2.x.x 或更高

# 检查 Docker 守护进程状态
docker ps
# 预期输出: 显示当前运行的容器列表 (可能为空)
```

---

## 架构说明

### 服务架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Network                          │
│                    (tfboys-network)                          │
│                                                               │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Redis   │   │   API    │   │    AI    │   │  Video   │ │
│  │  :6379   │◄──│ Gateway  │◄──│ Service  │◄──│ Service  │ │
│  │          │   │  :8001   │   │  :8002   │   │  :8003   │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       ▲              │               │               │       │
│       │              │               │               │       │
│       │         ┌────┴────┐     ┌────┴────┐     ┌────┴────┐ │
│       │         │ Celery  │     │ Celery  │     │ Celery  │ │
│       └─────────┤ Worker  │     │ Worker  │     │ Worker  │ │
│                 │   (AI)  │     │   (AI)  │     │ (Video) │ │
│                 └─────────┘     └─────────┘     └─────────┘ │
│                                                               │
│  共享存储卷 (tfboys-storage): /tmp/tfboys                    │
└─────────────────────────────────────────────────────────────┘
```

### 服务说明

| 服务名称 | 容器名称 | 端口 | 说明 |
|---------|---------|------|------|
| redis | tfboys-redis | 6379 | Redis 数据库 (任务状态、队列) |
| api-gateway | tfboys-api-gateway | 8001 | API 网关服务 |
| ai-service | tfboys-ai-service | 8002 | AI 处理服务 (文本分析、图像生成、TTS) |
| ai-worker | tfboys-ai-worker | - | AI Service Celery Worker |
| video-service | tfboys-video-service | 8003 | 视频合成服务 |
| video-worker | tfboys-video-worker | - | Video Service Celery Worker |
| frontend | tfboys-frontend | 3000 | 前端服务 |

### 共享资源

#### 1. 网络
- **网络名称**: `tfboys-network`
- **类型**: bridge
- **说明**: 所有服务在同一网络中，可通过服务名互相访问

#### 2. 存储卷
- **redis-data**: Redis 数据持久化
- **tfboys-storage**: 共享文件存储 (`/tmp/tfboys`)
  - 场景图像: `/tmp/tfboys/scenes/`
  - 配音文件: `/tmp/tfboys/audio/`
  - 生成视频: `/tmp/tfboys/videos/`

#### 3. Redis
- **连接方式**: `redis://redis:6379/0`
- **用途**:
  - 任务状态存储
  - Celery 消息队列
  - Celery 结果后端

---

## 快速开始

### 1. 克隆仓库

```bash
# 克隆项目代码
git clone https://github.com/qn-hackathon/tfboys.git
cd tfboys
```

### 2. 配置环境变量

```bash
# 复制 AI Service 环境变量模板
cp backend/ai-service/.env.example backend/ai-service/.env

# 编辑配置文件，填写真实的 API Key
vim backend/ai-service/.env
# 或使用其他编辑器: nano, code 等
```

**重要配置项**:
```bash
# 必须配置 - 七牛 AI Token API Key
QINIU_API_KEY=sk-xxxxxxxxxxxxxxxx  # 替换为真实的 Key

# 其他配置已预设为 Docker 环境默认值，无需修改
REDIS_URL=redis://redis:6379/0
VIDEO_SERVICE_URL=http://video-service:8003
LOCAL_STORAGE_DIR=/tmp/tfboys
```

### 3. 启动所有服务

```bash
# 构建并启动所有服务 (首次启动或代码更新后)
docker compose up --build -d

# 或者，如果镜像已存在且无需重新构建
docker compose up -d
```

### 4. 验证服务状态

```bash
# 查看所有容器状态
docker compose ps

# 预期输出: 所有服务状态为 "running" 或 "Up"
```

---

## 详细部署步骤

### 步骤 1: 准备工作

#### 1.1 检查端口占用

```bash
# 检查必要端口是否被占用
sudo netstat -tulpn | grep -E ':(6379|8001|8002|8003|3000)'

# 或使用 lsof (macOS/Linux)
lsof -i :6379
lsof -i :8001
lsof -i :8002
lsof -i :8003
lsof -i :3000
```

**解决方案**: 如果端口被占用，停止占用端口的服务或修改 `docker-compose.yml` 中的端口映射

#### 1.2 清理旧容器 (如果存在)

```bash
# 停止并删除旧的容器
docker compose down

# (可选) 删除所有相关卷 (会清空数据)
docker compose down -v
```

### 步骤 2: 配置服务

#### 2.1 配置 AI Service

```bash
# 1. 复制环境变量模板
cp backend/ai-service/.env.example backend/ai-service/.env

# 2. 编辑配置文件
vim backend/ai-service/.env
```

**配置说明**:

```bash
# === 必填配置 ===
QINIU_API_KEY=sk-your-actual-api-key-here  # ⚠️ 必须填写真实的 Key

# === Docker 环境默认配置 (无需修改) ===
REDIS_URL=redis://redis:6379/0              # Redis 连接地址
VIDEO_SERVICE_URL=http://video-service:8003  # Video Service 地址
LOCAL_STORAGE_DIR=/tmp/tfboys                # 本地存储目录
```

#### 2.2 配置 Video Service (如果需要)

```bash
# 1. 复制环境变量模板 (如果还没有 .env 文件)
cp backend/video-service/.env.example backend/video-service/.env

# 2. 编辑配置文件
vim backend/video-service/.env
```

### 步骤 3: 构建 Docker 镜像

```bash
# 构建所有服务的镜像
docker compose build

# 或构建单个服务
docker compose build ai-service
docker compose build video-service
```

**构建过程说明**:
- AI Service: 安装 Python 依赖 (FastAPI, Celery, OpenAI SDK 等)
- Video Service: 安装 FFmpeg、字体等系统依赖

**预期输出**:
```
[+] Building 45.2s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 37B
 => [internal] load .dockerignore
 ...
 => => naming to docker.io/library/tfboys-ai-service
```

### 步骤 4: 启动服务

#### 4.1 启动所有服务

```bash
# 后台启动所有服务
docker compose up -d

# 查看启动日志
docker compose logs -f
# 按 Ctrl+C 退出日志查看 (不会停止服务)
```

#### 4.2 分步启动 (推荐用于调试)

```bash
# 1. 先启动 Redis
docker compose up -d redis

# 2. 等待 Redis 健康检查通过
docker compose ps redis
# 状态应为 "healthy"

# 3. 启动 AI Service 和 Video Service
docker compose up -d ai-service video-service

# 4. 启动 Celery Workers
docker compose up -d ai-worker video-worker

# 5. 启动 API Gateway
docker compose up -d api-gateway

# 6. (可选) 启动前端
docker compose up -d frontend
```

### 步骤 5: 验证服务健康状态

```bash
# 1. 检查所有容器状态
docker compose ps

# 预期输出:
# NAME                    STATUS              PORTS
# tfboys-redis            Up (healthy)        0.0.0.0:6379->6379/tcp
# tfboys-ai-service       Up (healthy)        0.0.0.0:8002->8002/tcp
# tfboys-ai-worker        Up                  
# tfboys-video-service    Up (healthy)        0.0.0.0:8003->8003/tcp
# tfboys-video-worker     Up                  

# 2. 测试 AI Service 健康检查
curl http://localhost:8002/health
# 预期输出: {"status":"healthy"}

# 3. 测试 Video Service 健康检查
curl http://localhost:8003/health
# 预期输出: {"status":"healthy"}

# 4. 测试 API Gateway
curl http://localhost:8001/
# 预期输出: {"message":"TFBoys API Gateway","version":"1.0.0"}

# 5. 测试 Redis 连接
docker exec tfboys-redis redis-cli ping
# 预期输出: PONG
```

---

## 测试验证

### 方式一: 使用脚本测试 (推荐)

#### 1. 准备测试脚本

AI Service 已内置端到端测试脚本 `test_e2e.sh`

```bash
# 进入 AI Service 目录
cd backend/ai-service

# 查看脚本内容
cat test_e2e.sh
```

#### 2. 运行测试

```bash
# 方式 1: 直接在宿主机运行 (需要 curl 和 jq)
./test_e2e.sh

# 方式 2: 在 Docker 容器内运行
docker exec -it tfboys-ai-service bash -c "./test_e2e.sh"
```

#### 3. 预期输出

```
🎬 AI Service 端到端测试
================================

1. 检查 AI Service 是否运行...
✅ AI Service 正在运行

2. 创建视频生成任务...
✅ 任务创建成功
任务ID: test_1730000000
响应: {"task_id":"test_1730000000","status":"queued"}

3. 检查任务状态 (任务ID: test_1730000000)...
[尝试 1/60] 状态: processing
[尝试 2/60] 状态: processing
[尝试 3/60] 状态: processing
...
[尝试 15/60] 状态: completed
✅ 任务完成!
完整响应:
{
  "task_id": "test_1730000000",
  "status": "completed",
  "video_url": "/tmp/tfboys/videos/test_1730000000/final.mp4",
  "progress": {
    "text_analysis": "completed",
    "image_generation": "completed",
    "voice_generation": "completed",
    "video_composition": "completed"
  }
}
```

### 方式二: 手动 API 测试

#### 1. 创建测试任务

```bash
# 定义测试文本
TEST_NOVEL="小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。"

# 创建任务
TASK_ID="test_$(date +%s)"

curl -X POST http://localhost:8002/internal/tasks \
  -H "Content-Type: application/json" \
  -d "{
    \"task_id\": \"${TASK_ID}\",
    \"novel_text\": \"${TEST_NOVEL}\"
  }"

# 预期输出: {"task_id":"test_xxxxx","status":"queued"}
```

#### 2. 查询任务状态

```bash
# 使用上一步返回的 task_id
curl http://localhost:8002/internal/tasks/${TASK_ID}

# 预期输出 (处理中):
# {
#   "task_id": "test_xxxxx",
#   "status": "processing",
#   "progress": {
#     "text_analysis": "completed",
#     "image_generation": "processing",
#     "voice_generation": "pending",
#     "video_composition": "pending"
#   }
# }

# 预期输出 (完成):
# {
#   "task_id": "test_xxxxx",
#   "status": "completed",
#   "video_url": "/tmp/tfboys/videos/test_xxxxx/final.mp4",
#   "progress": {...}
# }
```

#### 3. 验证生成文件

```bash
# 查看任务相关的文件
docker exec tfboys-ai-service ls -lh /tmp/tfboys/scenes/
docker exec tfboys-ai-service ls -lh /tmp/tfboys/audio/${TASK_ID}/
docker exec tfboys-video-service ls -lh /tmp/tfboys/videos/${TASK_ID}/

# 预期输出:
# scenes/: 场景图像 (*.png)
# audio/: 配音文件 (*.mp3)
# videos/: 最终视频 (final.mp4)
```

### 方式三: 使用 Python 测试脚本

```bash
# 在 ai-service 容器中运行内置测试脚本
docker exec -it tfboys-ai-service python test_ai_service_workflow.py

# 或在宿主机运行 (需要安装依赖)
cd backend/ai-service
python test_ai_service_workflow.py
```

---

## 常见问题

### 1. 容器启动失败

**问题**: `docker compose up` 后某些容器状态为 `Exited`

**排查步骤**:

```bash
# 查看容器日志
docker compose logs ai-service
docker compose logs ai-worker

# 查看详细错误信息
docker compose logs --tail=100 ai-service
```

**常见原因**:
- **端口冲突**: 检查端口是否被占用 (见"步骤 1.1")
- **环境变量缺失**: 检查 `.env` 文件是否存在且配置正确
- **依赖服务未启动**: 确保 Redis 先启动并处于 `healthy` 状态

### 2. Redis 连接失败

**问题**: 服务日志显示 `ConnectionRefusedError: [Errno 111] Connection refused`

**解决方案**:

```bash
# 1. 检查 Redis 容器状态
docker compose ps redis

# 2. 检查 Redis 健康状态
docker exec tfboys-redis redis-cli ping
# 应输出: PONG

# 3. 如果 Redis 未启动，重启服务
docker compose restart redis

# 4. 等待 Redis 健康检查通过
docker compose ps redis
# 状态应变为 "healthy"
```

### 3. API 调用返回 500 错误

**问题**: 测试 API 时返回 `{"detail":"Internal Server Error"}`

**排查步骤**:

```bash
# 1. 查看服务日志
docker compose logs -f ai-service

# 2. 检查 QINIU_API_KEY 是否配置
docker exec tfboys-ai-service env | grep QINIU_API_KEY

# 3. 手动进入容器调试
docker exec -it tfboys-ai-service bash
python -c "from app.config import settings; print(settings.qiniu_api_key)"
```

### 4. Celery Worker 无法消费任务

**问题**: 任务状态一直是 `queued`，未被处理

**排查步骤**:

```bash
# 1. 检查 Worker 状态
docker compose logs -f ai-worker

# 2. 检查 Celery 是否连接到 Redis
docker exec tfboys-ai-worker celery -A app.workers.celery_app inspect active

# 3. 重启 Worker
docker compose restart ai-worker
```

### 5. 共享存储卷权限问题

**问题**: 日志显示 `PermissionError: [Errno 13] Permission denied: '/tmp/tfboys/...'`

**解决方案**:

```bash
# 1. 进入容器检查权限
docker exec -it tfboys-ai-service ls -ld /tmp/tfboys

# 2. 如果权限不足，手动修复
docker exec -it tfboys-ai-service chmod -R 777 /tmp/tfboys

# 3. 或重新构建镜像 (Dockerfile 已包含权限设置)
docker compose build ai-service
docker compose up -d ai-service
```

---

## 运维管理

### 查看日志

```bash
# 查看所有服务日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f ai-service
docker compose logs -f ai-worker

# 查看最近 100 行日志
docker compose logs --tail=100 ai-service

# 查看从特定时间开始的日志
docker compose logs --since 2024-10-26T10:00:00 ai-service
```

### 重启服务

```bash
# 重启所有服务
docker compose restart

# 重启特定服务
docker compose restart ai-service
docker compose restart ai-worker

# 完全重建服务 (代码更新后)
docker compose up -d --build ai-service
```

### 停止服务

```bash
# 停止所有服务 (保留容器和数据)
docker compose stop

# 停止并删除容器 (保留数据卷)
docker compose down

# 停止并删除容器和数据卷 (⚠️ 会删除所有数据)
docker compose down -v
```

### 清理资源

```bash
# 清理未使用的 Docker 资源
docker system prune -a

# 清理未使用的卷
docker volume prune

# 清理 TFBoys 相关资源
docker compose down -v
docker rmi $(docker images 'tfboys*' -q)
```

### 扩展 Worker

```bash
# 动态增加 Worker 实例数
docker compose up -d --scale ai-worker=3

# 查看运行的 Worker
docker compose ps | grep worker
```

### 监控资源使用

```bash
# 查看容器资源使用情况
docker stats

# 查看特定容器
docker stats tfboys-ai-service tfboys-ai-worker
```

---

## 生产环境部署建议

### 1. 安全配置

```bash
# 使用 Docker Secrets 管理敏感信息
# 不要在 .env 文件中提交真实的 API Key

# 限制容器资源
# 在 docker-compose.yml 中添加:
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
    reservations:
      cpus: '1.0'
      memory: 2G
```

### 2. 日志管理

```bash
# 配置日志驱动
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 3. 高可用配置

- 使用 Redis Cluster 或 Redis Sentinel
- 配置多个 Celery Worker 实例
- 使用 Nginx 反向代理和负载均衡

### 4. 监控告警

- 部署 Prometheus + Grafana 监控 Docker 容器
- 配置 Celery Flower 监控任务队列
- 设置服务健康检查告警

---

## 附录

### A. 环境变量完整列表

| 变量名 | 说明 | 默认值 | 是否必填 |
|-------|------|--------|----------|
| REDIS_URL | Redis 连接地址 | redis://redis:6379/0 | 是 |
| VIDEO_SERVICE_URL | Video Service URL | http://video-service:8003 | 是 |
| LOCAL_STORAGE_DIR | 本地存储目录 | /tmp/tfboys | 是 |
| QINIU_API_KEY | 七牛 AI Token API Key | - | 是 |

### B. Docker Compose 命令速查

| 命令 | 说明 |
|------|------|
| `docker compose up -d` | 后台启动所有服务 |
| `docker compose up -d --build` | 重新构建并启动 |
| `docker compose down` | 停止并删除容器 |
| `docker compose down -v` | 停止并删除容器和卷 |
| `docker compose ps` | 查看服务状态 |
| `docker compose logs -f` | 查看实时日志 |
| `docker compose restart` | 重启服务 |
| `docker compose exec <service> bash` | 进入容器 |

### C. 故障排查清单

- [ ] Docker 和 Docker Compose 版本符合要求
- [ ] 所有必需端口未被占用
- [ ] `.env` 文件存在且配置正确
- [ ] QINIU_API_KEY 已填写真实值
- [ ] Redis 健康检查通过
- [ ] 服务日志无明显错误
- [ ] 网络连通性正常 (服务间可互相访问)
- [ ] 存储卷权限正确 (777 或 适当的用户权限)

---

**文档版本**: 1.0.0  
**最后更新**: 2025-10-26  
**维护者**: TFBoys Team

如有问题，请提交 Issue: https://github.com/qn-hackathon/tfboys/issues
