# Video Service Docker 快速启动指南

## 🎯 一键启动

```bash
cd backend/video-service

cp .env.example .env

nano .env

docker-compose up -d

./test_video_service.sh
```

## 📦 包含的服务

- **video-service**: FastAPI 服务 (端口 8003)
- **celery-worker**: Celery 异步任务处理器
- **redis**: Redis 数据库 (端口 6379)

## 🔧 核心配置

`.env` 文件包含以下配置（默认值已可用，可按需修改）：

```env
REDIS_URL=redis://redis:6379/0
LOCAL_STORAGE_DIR=/tmp/tfboys
FFMPEG_THREADS=4
CHINESE_FONT_PATH=/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
AI_SERVICE_CALLBACK_URL=http://ai-service:8002/callbacks/video-completed
```

## ✅ 验证服务

```bash
curl http://localhost:8003/health

docker-compose logs -f video-service

docker-compose ps
```

## 📖 详细文档

完整部署文档请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🧪 测试

运行自动化测试脚本：
```bash
./test_video_service.sh
```

访问 API 文档：
```
http://localhost:8003/docs
```

## 🛑 停止服务

```bash
docker-compose down

docker-compose down -v
```

## 🆘 常见问题

1. **端口被占用**：修改 docker-compose.yml 中的端口映射
2. **FFmpeg 未安装**：重新构建镜像 `docker-compose build --no-cache`
3. **Redis 连接失败**：检查 Redis 容器状态 `docker-compose ps`

详细故障排查请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)
