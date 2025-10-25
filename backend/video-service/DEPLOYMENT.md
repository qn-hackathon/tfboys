# Video Service Docker 部署指南

本文档提供 video-service 完整的 Docker 测试环境部署步骤。

## 📋 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

## 🚀 快速开始

### 步骤 1: 准备配置文件

```bash
cd backend/video-service
cp .env.example .env
```

编辑 `.env` 文件，填入真实的配置信息：

```bash
nano .env
```

**必需配置**：
- `OSS_ACCESS_KEY`: 阿里云 OSS Access Key
- `OSS_SECRET_KEY`: 阿里云 OSS Secret Key
- `OSS_BUCKET`: OSS 存储桶名称

**可选配置**：
- `FFMPEG_THREADS`: FFmpeg 线程数（默认 4）
- `AI_SERVICE_CALLBACK_URL`: AI 服务回调 URL

### 步骤 2: 构建 Docker 镜像

```bash
docker-compose build
```

这将：
- 拉取 Python 3.11 基础镜像
- 安装 FFmpeg 和中文字体
- 安装 Python 依赖包
- 创建工作目录和临时文件目录

### 步骤 3: 启动服务

```bash
docker-compose up -d
```

这将启动三个容器：
1. **redis**: Redis 数据库（端口 6379）
2. **video-service**: FastAPI 服务（端口 8003）
3. **celery-worker**: Celery 异步任务处理器

### 步骤 4: 验证服务状态

```bash
docker-compose ps
```

预期输出：
```
NAME                          COMMAND                  SERVICE         STATUS
video-service                 "uvicorn app.main:ap…"   video-service   Up
video-service-celery-worker   "celery -A app.worke…"   celery-worker   Up
video-service-redis           "docker-entrypoint.s…"   redis           Up (healthy)
```

检查服务健康状态：

```bash
curl http://localhost:8003/health
```

预期响应：
```json
{"status": "healthy"}
```

## 🔍 详细操作命令

### 查看日志

查看所有服务日志：
```bash
docker-compose logs -f
```

查看特定服务日志：
```bash
docker-compose logs -f video-service
docker-compose logs -f celery-worker
docker-compose logs -f redis
```

### 进入容器

进入 video-service 容器：
```bash
docker-compose exec video-service bash
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

重启特定服务：
```bash
docker-compose restart video-service
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

### 查看资源占用

查看容器资源使用情况：
```bash
docker stats
```

### 更新服务

当代码更新后：
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## 🧪 测试方法

### 1. 健康检查测试

```bash
curl http://localhost:8003/health
```

### 2. API 文档测试

在浏览器中访问：
```
http://localhost:8003/docs
```

### 3. FFmpeg 功能测试

进入容器验证 FFmpeg：
```bash
docker-compose exec video-service ffmpeg -version
```

### 4. 字体支持测试

验证中文字体安装：
```bash
docker-compose exec video-service fc-list | grep -i wqy
```

### 5. Redis 连接测试

```bash
docker-compose exec redis redis-cli ping
```

预期输出：`PONG`

### 6. 完整视频合成测试

使用测试脚本发送请求：

```bash
curl -X POST "http://localhost:8003/internal/compose" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_001",
    "scenes": [
      {
        "scene_id": "scene_001",
        "image_url": "https://example.com/image1.jpg",
        "audio_url": "https://example.com/audio1.mp3",
        "subtitle": "这是第一个场景的字幕",
        "duration": 5.0
      }
    ],
    "output_filename": "test_video.mp4"
  }'
```

### 7. Celery 任务测试

查看 Celery Worker 状态：
```bash
docker-compose exec celery-worker celery -A app.workers.celery_app inspect active
```

查看任务队列：
```bash
docker-compose exec celery-worker celery -A app.workers.celery_app inspect active_queues
```

## 📊 测试示例

### 示例 1: 单场景视频合成

```bash
cat > test_single_scene.json <<EOF
{
  "task_id": "test_single_001",
  "scenes": [
    {
      "scene_id": "scene_001",
      "image_url": "https://picsum.photos/1920/1080",
      "audio_url": "https://example.com/audio.mp3",
      "subtitle": "欢迎来到TFBoys视频生成系统",
      "duration": 3.0
    }
  ],
  "output_filename": "single_scene_test.mp4"
}
EOF

curl -X POST "http://localhost:8003/internal/compose" \
  -H "Content-Type: application/json" \
  -d @test_single_scene.json
```

### 示例 2: 多场景视频合成

```bash
cat > test_multi_scenes.json <<EOF
{
  "task_id": "test_multi_001",
  "scenes": [
    {
      "scene_id": "scene_001",
      "image_url": "https://picsum.photos/1920/1080?random=1",
      "audio_url": "https://example.com/audio1.mp3",
      "subtitle": "第一个场景",
      "duration": 3.0
    },
    {
      "scene_id": "scene_002",
      "image_url": "https://picsum.photos/1920/1080?random=2",
      "audio_url": "https://example.com/audio2.mp3",
      "subtitle": "第二个场景",
      "duration": 3.0
    },
    {
      "scene_id": "scene_003",
      "image_url": "https://picsum.photos/1920/1080?random=3",
      "audio_url": "https://example.com/audio3.mp3",
      "subtitle": "第三个场景",
      "duration": 3.0
    }
  ],
  "output_filename": "multi_scene_test.mp4"
}
EOF

curl -X POST "http://localhost:8003/internal/compose" \
  -H "Content-Type: application/json" \
  -d @test_multi_scenes.json
```

### 示例 3: 无字幕视频合成

```bash
curl -X POST "http://localhost:8003/internal/compose" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_no_subtitle_001",
    "scenes": [
      {
        "scene_id": "scene_001",
        "image_url": "https://picsum.photos/1920/1080",
        "audio_url": "https://example.com/audio.mp3",
        "duration": 5.0
      }
    ],
    "output_filename": "no_subtitle_test.mp4"
  }'
```

## 🐛 故障排查

### 问题 1: 容器无法启动

**症状**：`docker-compose up -d` 失败

**解决方案**：
```bash
docker-compose logs video-service
docker-compose logs celery-worker
```

常见原因：
- 端口被占用（检查 8003 端口）
- 配置文件错误（检查 .env 文件）

### 问题 2: FFmpeg 命令失败

**症状**：视频合成任务失败，日志显示 FFmpeg 错误

**解决方案**：
```bash
docker-compose exec video-service ffmpeg -version
```

如果 FFmpeg 未安装：
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 问题 3: 中文字幕显示异常

**症状**：字幕出现乱码或方框

**解决方案**：
```bash
docker-compose exec video-service ls -la /usr/share/fonts/truetype/wqy/
```

确保 `wqy-zenhei.ttc` 存在。

### 问题 4: Redis 连接失败

**症状**：服务日志显示 Redis 连接错误

**解决方案**：
```bash
docker-compose exec redis redis-cli ping
```

如果无响应：
```bash
docker-compose restart redis
```

### 问题 5: OSS 上传失败

**症状**：视频生成成功但上传失败

**解决方案**：
1. 检查 OSS 配置是否正确
2. 检查网络连接
3. 验证 OSS 权限

```bash
docker-compose exec video-service python -c "
from app.services.oss_client import oss_client
print('OSS连接测试:', oss_client.bucket.bucket_name)
"
```

## 📈 性能优化建议

### 1. 增加 FFmpeg 线程数

对于多核 CPU，增加线程数可提升性能：
```bash
# .env 文件中
FFMPEG_THREADS=8
```

### 2. 增加 Celery Worker 并发数

编辑 `docker-compose.yml`：
```yaml
celery-worker:
  command: celery -A app.workers.celery_app worker --loglevel=info --concurrency=4
```

### 3. 使用 SSD 存储

将临时文件目录映射到 SSD：
```yaml
volumes:
  - /path/to/ssd/video-temp:/tmp/video-service
```

### 4. 限制内存使用

在 `docker-compose.yml` 中添加资源限制：
```yaml
video-service:
  deploy:
    resources:
      limits:
        memory: 2G
      reservations:
        memory: 1G
```

## 🔒 安全建议

1. **不要在生产环境中使用默认配置**
2. **使用环境变量管理敏感信息**
3. **定期更新 Docker 镜像**
4. **限制容器网络访问**
5. **使用 Docker secrets 管理密钥**（生产环境）

## 📚 更多资源

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [FFmpeg 文档](https://ffmpeg.org/documentation.html)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [Celery 文档](https://docs.celeryproject.org/)

## 🆘 获取帮助

如遇到问题，请：
1. 查看容器日志：`docker-compose logs -f`
2. 检查环境配置：`.env` 文件
3. 查看 API 文档：http://localhost:8003/docs
4. 提交 Issue 到项目仓库

---

**最后更新**: 2024-10-25
**维护者**: TFBoys Team
