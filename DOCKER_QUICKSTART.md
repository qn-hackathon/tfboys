# AI Service Docker 快速启动指南

本文档提供 AI Service Docker 测试环境的快速启动方法。

---

## 🚀 一键部署 (推荐)

### 使用自动化部署脚本

```bash
# 在项目根目录执行
./deploy-docker.sh
```

脚本会自动完成:
1. ✅ 环境检查 (Docker, Docker Compose, 端口)
2. ✅ 配置环境变量
3. ✅ 构建 Docker 镜像
4. ✅ 启动所有服务
5. ✅ 验证服务健康状态
6. ✅ (可选) 运行端到端测试

---

## 📝 手动部署

### 1. 配置环境变量

```bash
# 复制模板
cp backend/ai-service/.env.example backend/ai-service/.env

# 编辑配置，填写 QINIU_API_KEY
vim backend/ai-service/.env
```

### 2. 启动服务

```bash
# 构建并启动
docker compose up --build -d

# 查看状态
docker compose ps
```

### 3. 验证服务

```bash
# 测试 AI Service
curl http://localhost:8002/health

# 测试 Video Service
curl http://localhost:8003/health

# 测试 API Gateway
curl http://localhost:8001/
```

---

## 🧪 测试方法

### 方式一: 使用内置测试脚本

```bash
docker exec -it tfboys-ai-service ./test_e2e.sh
```

### 方式二: 手动 API 测试

```bash
# 创建任务
TASK_ID="test_$(date +%s)"
curl -X POST http://localhost:8002/internal/tasks \
  -H "Content-Type: application/json" \
  -d "{
    \"task_id\": \"${TASK_ID}\",
    \"novel_text\": \"小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。\"
  }"

# 查询任务状态
curl http://localhost:8002/internal/tasks/${TASK_ID}
```

---

## 🔧 常用命令

### 服务管理

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
docker compose logs -f ai-service
docker compose logs -f ai-worker

# 重启服务
docker compose restart
docker compose restart ai-service

# 停止服务
docker compose stop

# 删除服务 (保留数据)
docker compose down

# 删除服务和数据
docker compose down -v
```

### 进入容器调试

```bash
# 进入 AI Service 容器
docker exec -it tfboys-ai-service bash

# 进入 Redis 容器
docker exec -it tfboys-redis redis-cli

# 进入 Worker 容器
docker exec -it tfboys-ai-worker bash
```

### 查看资源使用

```bash
# 实时监控
docker stats

# 查看磁盘使用
docker system df
```

---

## ❓ 常见问题

### 1. 端口被占用

```bash
# 查看端口占用
lsof -i :8002
lsof -i :6379

# 停止占用端口的进程或修改 docker-compose.yml 中的端口映射
```

### 2. 服务无法启动

```bash
# 查看详细日志
docker compose logs --tail=100 ai-service

# 检查环境变量
docker exec tfboys-ai-service env | grep QINIU_API_KEY

# 重新构建
docker compose up --build -d
```

### 3. Redis 连接失败

```bash
# 检查 Redis 状态
docker compose ps redis

# 重启 Redis
docker compose restart redis

# 测试连接
docker exec tfboys-redis redis-cli ping
```

### 4. API 返回 500 错误

```bash
# 检查服务日志
docker compose logs -f ai-service

# 验证 API Key 配置
docker exec tfboys-ai-service bash -c "python -c 'from app.config import settings; print(settings.qiniu_api_key)'"
```

---

## 📚 更多信息

- **详细部署文档**: 见 `DOCKER_DEPLOYMENT_GUIDE.md`
- **架构说明**: 见部署指南中的"架构说明"章节
- **故障排查**: 见部署指南中的"常见问题"章节

---

## 🎯 服务端点

| 服务 | 端口 | 健康检查 |
|------|------|----------|
| API Gateway | 8001 | http://localhost:8001/ |
| AI Service | 8002 | http://localhost:8002/health |
| Video Service | 8003 | http://localhost:8003/health |
| Frontend | 3000 | http://localhost:3000 |
| Redis | 6379 | `docker exec tfboys-redis redis-cli ping` |

---

**快速开始**: `./deploy-docker.sh`  
**停止服务**: `docker compose down`  
**查看日志**: `docker compose logs -f`  
**运行测试**: `docker exec -it tfboys-ai-service ./test_e2e.sh`
