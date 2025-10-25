# Video Service 功能测试指南

本文档提供 TFBoys Video Service 的完整测试方案，包括测试数据、测试步骤和详细命令。

## 📦 测试数据清单

### 1. 测试图片

所有测试图片均为 1920x1080 分辨率的 JPG 格式，适合视频合成测试。

| 文件名 | 用途 | 尺寸 | 说明 |
|--------|------|------|------|
| `scene_1.jpg` | 场景1图像 | 1920x1080 | 蓝色背景，白色矩形 |
| `scene_2.jpg` | 场景2图像 | 1920x1080 | 粉色背景，黄色圆形 |
| `scene_3.jpg` | 场景3图像 | 1920x1080 | 绿色背景，红色三角形 |
| `character_xiaoming.jpg` | 角色参考图 | 512x512 | 简化的角色肖像 |

**文件位置**: `/workspace/test-data/video-service/`

**下载方式**:
```bash
# 从仓库下载
cd /workspace/test-data/video-service/
ls -lh *.jpg
```

### 2. 测试音频

由于当前环境限制，音频文件需要使用以下方式生成：

#### 方式 1: 使用 FFmpeg 生成（推荐）

```bash
# 场景1音频 (3秒，440Hz)
ffmpeg -f lavfi -i "sine=frequency=440:duration=3" \
  -ar 44100 -ac 2 -b:a 192k scene_1_audio.mp3 -y

# 场景2音频 (4秒，523Hz)
ffmpeg -f lavfi -i "sine=frequency=523:duration=4" \
  -ar 44100 -ac 2 -b:a 192k scene_2_audio.mp3 -y

# 场景3音频 (5秒，659Hz)
ffmpeg -f lavfi -i "sine=frequency=659:duration=5" \
  -ar 44100 -ac 2 -b:a 192k scene_3_audio.mp3 -y
```

#### 方式 2: 使用在线 TTS 服务

可以使用七牛云 TTS 或其他 TTS 服务生成真实的配音：

- 场景1文本: "在一个阳光明媚的早晨，小明走在上学的路上"
- 场景2文本: "突然，他发现前方的桥梁被大雨冲垮了"
- 场景3文本: "小明决定绕道而行，最终按时到达了学校"

#### 方式 3: 下载示例音频

从公开音频库下载测试用音频：
```bash
# 示例 URL（需替换为实际可用的音频 URL）
wget https://example.com/test-audio-3s.mp3 -O scene_1_audio.mp3
wget https://example.com/test-audio-4s.mp3 -O scene_2_audio.mp3
wget https://example.com/test-audio-5s.mp3 -O scene_3_audio.mp3
```

### 3. 测试请求数据

**文件**: `test_request.json`

完整的 API 请求 JSON，包含 3 个场景的完整数据结构。

---

## 🚀 测试环境准备

### 前置条件

1. **Docker 和 Docker Compose**: 已安装并运行
2. **Redis**: 已启动（端口 6379）
3. **环境变量**: 已配置 `.env` 文件

### 启动服务

#### 方式 1: 使用 Docker Compose（推荐）

```bash
cd /workspace/backend/video-service

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f video-service
```

#### 方式 2: 本地开发模式

```bash
cd /workspace/backend/video-service

# 安装依赖
pip install -r requirements.txt

# 确保 Redis 已启动
redis-cli ping

# 启动 Video Service
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

# 另开终端，启动 Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

### 验证服务状态

```bash
# 健康检查
curl http://localhost:8003/health

# 预期响应:
# {"status":"healthy"}

# API 文档
curl http://localhost:8003/docs
# 或在浏览器访问: http://localhost:8003/docs
```

---

## 🧪 测试步骤

### 测试 1: 基础功能测试

运行项目自带的测试脚本：

```bash
cd /workspace/backend/video-service
chmod +x test_video_service.sh
./test_video_service.sh
```

**测试内容**:
- ✅ 健康检查
- ✅ 根路径访问
- ✅ FFmpeg 版本检查
- ✅ 中文字体检查
- ✅ Redis 连接检查
- ✅ Python 依赖检查
- ✅ 本地存储目录权限
- ✅ API 文档访问
- ✅ Celery Worker 状态

### 测试 2: API 接口测试

#### 2.1 创建视频合成任务

**步骤 1: 准备测试数据**

确保图片和音频文件已准备好，或使用在线 URL。

**步骤 2: 修改 test_request.json**

将 `test_request.json` 中的 URL 替换为实际可访问的 URL：

```json
{
  "image_url": "https://your-storage.com/scene_1.jpg",
  "audio_url": "https://your-storage.com/scene_1_audio.mp3"
}
```

**步骤 3: 发送创建任务请求**

```bash
curl -X POST http://localhost:8003/internal/video-synthesis/jobs \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

**预期响应**:
```json
{
  "code": 0,
  "message": "视频合成任务已创建",
  "data": {
    "job_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "task_id": "test_task_001",
    "status": "pending"
  }
}
```

**保存 job_id** 用于后续查询。

#### 2.2 查询任务状态

```bash
# 替换 <job_id> 为上一步返回的 job_id
JOB_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

curl http://localhost:8003/internal/video-synthesis/jobs/$JOB_ID
```

**任务状态说明**:

| 状态 | 说明 |
|------|------|
| `pending` | 任务已创建，等待处理 |
| `processing` | 正在处理视频合成 |
| `completed` | 任务完成 |
| `failed` | 任务失败 |

**处理中的响应示例**:
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "job_id": "...",
    "task_id": "test_task_001",
    "status": "processing",
    "progress": {
      "current_scene": 1,
      "total_scenes": 3
    }
  }
}
```

**完成后的响应示例**:
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "job_id": "...",
    "task_id": "test_task_001",
    "status": "completed",
    "result": {
      "video_url": "/tmp/tfboys/videos/test_task_001/final.mp4",
      "duration": 12.0,
      "file_size": 1048576,
      "thumbnail_url": null
    }
  }
}
```

#### 2.3 轮询任务状态（脚本示例）

```bash
#!/bin/bash
JOB_ID="your-job-id-here"
MAX_WAIT=300  # 最多等待 5 分钟
INTERVAL=5    # 每 5 秒查询一次

elapsed=0
while [ $elapsed -lt $MAX_WAIT ]; do
  response=$(curl -s http://localhost:8003/internal/video-synthesis/jobs/$JOB_ID)
  status=$(echo $response | jq -r '.data.status')
  
  echo "[$(date '+%H:%M:%S')] 任务状态: $status"
  
  if [ "$status" = "completed" ]; then
    echo "✅ 任务完成！"
    echo $response | jq '.data.result'
    exit 0
  elif [ "$status" = "failed" ]; then
    echo "❌ 任务失败！"
    echo $response | jq '.data.error'
    exit 1
  fi
  
  sleep $INTERVAL
  elapsed=$((elapsed + INTERVAL))
done

echo "⏰ 超时: 任务未在 $MAX_WAIT 秒内完成"
exit 1
```

### 测试 3: 下载和验证视频

```bash
# 假设任务完成，video_url 为 /tmp/tfboys/videos/test_task_001/final.mp4

# 方式 1: 从 Docker 容器复制出来
docker cp video-service:/tmp/tfboys/videos/test_task_001/final.mp4 ./test_output.mp4

# 方式 2: 直接在容器内播放（需要支持 X11）
docker exec -it video-service ffplay /tmp/tfboys/videos/test_task_001/final.mp4

# 方式 3: 使用 ffprobe 查看视频信息
docker exec -it video-service ffprobe -v quiet -print_format json -show_format -show_streams \
  /tmp/tfboys/videos/test_task_001/final.mp4
```

**验证项**:
- ✅ 视频时长约为 12 秒（3+4+5）
- ✅ 分辨率为 1920x1080
- ✅ 帧率为 30 fps
- ✅ 包含 3 个场景
- ✅ 字幕显示正确
- ✅ 音频正常

---

## 🛠️ 高级测试

### 测试 4: 自定义视频配置

修改 `test_request.json` 中的 `video_config`:

```json
{
  "video_config": {
    "resolution": "1280x720",
    "fps": 24,
    "transition_effect": "dissolve",
    "subtitle_style": {
      "font_size": 40,
      "color": "yellow",
      "position": "top",
      "font_family": "WenQuanYi Micro Hei",
      "border_width": 3,
      "border_color": "red"
    }
  }
}
```

### 测试 5: 压力测试

并发创建多个任务：

```bash
#!/bin/bash
for i in {1..10}; do
  curl -X POST http://localhost:8003/internal/video-synthesis/jobs \
    -H "Content-Type: application/json" \
    -d @test_request.json &
done
wait
echo "✅ 10 个任务已提交"
```

### 测试 6: 错误处理测试

#### 6.1 测试无效的 job_id

```bash
curl http://localhost:8003/internal/video-synthesis/jobs/invalid-job-id
```

**预期响应**:
```json
{
  "detail": "任务不存在"
}
```

#### 6.2 测试缺失字段

```bash
curl -X POST http://localhost:8003/internal/video-synthesis/jobs \
  -H "Content-Type: application/json" \
  -d '{"task_id": "test"}'
```

**预期响应**: 422 Validation Error

---

## 📊 监控和调试

### 查看服务日志

```bash
# Video Service 日志
docker-compose logs -f video-service

# Celery Worker 日志
docker-compose logs -f celery-worker

# Redis 日志
docker-compose logs -f redis
```

### 检查 Redis 数据

```bash
# 进入 Redis
redis-cli

# 查看所有视频任务
KEYS video_job:*

# 查看特定任务
GET video_job:<job_id>
```

### 检查本地存储

```bash
# 查看生成的视频文件
docker exec -it video-service ls -lh /tmp/tfboys/videos/

# 查看临时文件
docker exec -it video-service ls -lh /tmp/tfboys/temp/
```

---

## 🐛 常见问题

### 1. Celery Worker 未运行

**症状**: 任务一直处于 `pending` 状态

**解决方案**:
```bash
# 检查 Celery Worker 状态
docker-compose ps celery-worker

# 重启 Celery Worker
docker-compose restart celery-worker

# 查看 Celery Worker 日志
docker-compose logs celery-worker
```

### 2. FFmpeg 错误

**症状**: 任务失败，错误信息包含 "ffmpeg"

**解决方案**:
```bash
# 检查 FFmpeg 安装
docker exec -it video-service ffmpeg -version

# 如果未安装，重新构建镜像
docker-compose build video-service
```

### 3. 中文字幕显示为方框

**症状**: 视频中的中文字幕显示为方框或乱码

**解决方案**:
```bash
# 检查中文字体
docker exec -it video-service fc-list | grep -i wqy

# 如果没有字体，安装
docker exec -it video-service apt-get update && apt-get install -y fonts-wqy-microhei
```

### 4. 存储目录权限问题

**症状**: 任务失败，错误信息包含 "Permission denied"

**解决方案**:
```bash
# 修复目录权限
docker exec -it video-service chmod -R 777 /tmp/tfboys
```

### 5. Redis 连接失败

**症状**: 任务无法创建或查询

**解决方案**:
```bash
# 检查 Redis 状态
docker-compose ps redis

# 测试 Redis 连接
redis-cli ping

# 检查 Redis URL 配置
docker exec -it video-service env | grep REDIS_URL
```

---

## 📈 性能基准

在标准配置下（Docker, 4 CPU, 8GB RAM）:

| 指标 | 参考值 |
|------|--------|
| 单个场景处理时间 | 2-5 秒 |
| 3 场景视频合成时间 | 10-20 秒 |
| 并发任务处理能力 | 5-10 个/分钟 |
| 内存占用 | 500MB - 1GB |

---

## 📚 参考资源

- [Video Service API 文档](http://localhost:8003/docs)
- [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)
- [Celery 官方文档](https://docs.celeryproject.org/)
- [项目 CLAUDE.md](/workspace/CLAUDE.md)

---

## 💡 测试建议

1. **从基础测试开始**: 先运行 `test_video_service.sh` 确保环境正常
2. **使用小数据集**: 初次测试使用 2-3 个场景
3. **逐步增加复杂度**: 先测试基本功能，再测试高级配置
4. **监控资源使用**: 使用 `docker stats` 监控容器资源
5. **保留日志**: 失败时保留完整日志用于调试

---

**最后更新**: 2025-10-25
**测试数据版本**: v1.0
