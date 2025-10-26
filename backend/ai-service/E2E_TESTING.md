# AI Service 端到端测试指南

## 📋 前置条件

### 1. 环境配置

确保已安装以下依赖：
- Python 3.9+
- Redis
- 七牛 AI Token API Key

### 2. 安装依赖

```bash
# 在项目根目录
pip install -e ./shared

# 在 ai-service 目录
cd backend/ai-service
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
cd backend/ai-service
cat > .env << 'EOF'
# 七牛 AI Token API Key (必需)
QINIU_API_KEY=your-qiniu-api-key

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# Video Service URL
VIDEO_SERVICE_URL=http://localhost:8003
EOF
```

**⚠️ 重要：** 将 `your-qiniu-api-key` 替换为你的真实七牛 AI Token API Key。

---

## 🚀 启动服务

需要**3个终端**分别运行以下服务：

### 终端 1: 启动 Redis

```bash
# 方式1: 使用 Docker Compose
docker-compose up -d redis

# 方式2: 使用 Docker 直接运行
docker run -d -p 6379:6379 redis:latest

# 方式3: 本地 Redis (如果已安装)
redis-server
```

验证 Redis 运行：
```bash
redis-cli ping
# 应该返回: PONG
```

### 终端 2: 启动 AI Service API

```bash
cd backend/ai-service

# 设置 PYTHONPATH
export PYTHONPATH="$(cd ../.. && pwd)"

# 启动 API 服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**预期输出:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### 终端 3: 启动 Celery Worker

```bash
cd backend/ai-service

# 设置 PYTHONPATH
export PYTHONPATH="$(cd ../.. && pwd)"

# 启动 Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

**预期输出:**
```
[tasks]
  . process_novel_task

[INFO/MainProcess] celery@yourhostname ready.
```

---

## 🧪 运行测试

### 方式1: 使用测试脚本

```bash
cd backend/ai-service
./test_e2e.sh
```

测试脚本将：
1. ✅ 检查 AI Service 是否运行
2. ✅ 创建视频生成任务
3. ✅ 轮询任务状态
4. ✅ 显示最终结果

### 方式2: 手动测试

#### 1. 发送测试请求

```bash
# 创建测试任务
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_001",
    "novel_text": "小明是一个活泼开朗的男孩。今天早上，小明起床后刷牙洗脸，然后去上学。路上他遇到了好朋友小红，两人一起走进教室。"
  }'
```

**成功响应示例:**
```json
{
  "task_id": "test_001",
  "status": "pending",
  "created_at": "2025-01-20T10:00:00"
}
```

#### 2. 检查任务状态

```bash
# 查询任务状态 (任务ID替换为你创建的)
curl http://localhost:8001/tasks/test_001
```

**可能的响应:**
- `pending` - 任务已创建，等待处理
- `analyzing` - 正在分析文本
- `generating_images` - 正在生成图像
- `generating_audio` - 正在生成配音
- `synthesizing_video` - 正在合成视频
- `completed` - 任务完成
- `failed` - 任务失败

#### 3. 查看日志

在 **终端2** (API服务) 和 **终端3** (Celery Worker) 查看详细处理日志。

---

## 📊 任务状态说明

| 状态 | 说明 |
|------|------|
| `pending` | 任务已创建，等待 Celery Worker 处理 |
| `analyzing` | 文本分析中，提取场景和角色 |
| `generating_images` | 生成场景图像 |
| `generating_audio` | 生成配音 |
| `synthesizing_video` | Video Service 合成视频中 |
| `completed` | 任务完成，视频已生成 |
| `failed` | 任务失败，检查错误信息 |

---

## 🔍 故障排查

### 问题 1: Celery Worker 无法连接到 Redis

**错误信息:**
```
Redis client initialization failed
```

**解决方法:**
```bash
# 检查 Redis 是否运行
redis-cli ping

# 重启 Redis
docker restart $(docker ps -q -f name=redis)
```

### 问题 2: "No module named 'shared'"

**解决方法:**
```bash
# 确保设置了 PYTHONPATH
export PYTHONPATH="$(cd ../.. && pwd)"

# 确认 shared 模块已安装
python3 -c "import shared; print(shared.__file__)"
```

### 问题 3: API Key 错误

**错误信息:**
```
Failed to call Qiniu API: 401 Unauthorized
```

**解决方法:**
检查 `.env` 文件中的 `QINIU_API_KEY` 是否正确设置。

### 问题 4: 任务一直处于 pending 状态

**可能原因:**
- Celery Worker 未启动
- Redis 连接问题

**解决方法:**
```bash
# 检查 Celery Worker 是否运行
ps aux | grep celery

# 重启 Celery Worker (在终端3)
# 按 Ctrl+C 停止，然后重新启动
```

---

## 📈 监控任务进度

### 使用 API 查询

```bash
# 获取任务详细信息
curl http://localhost:8001/tasks/test_001 | jq '.'

# 获取任务进度
curl http://localhost:8001/tasks/test_001 | jq '.progress'
```

### 查看 Redis 数据

```bash
# 连接到 Redis
redis-cli

# 查看所有任务
KEYS task:*

# 查看特定任务数据
GET task:test_001

# 退出
exit
```

### 查看 Celery 任务

```bash
# 在 Celery Worker 终端中查看任务列表
celery -A app.workers.celery_app inspect active

# 查看已注册的任务
celery -A app.workers.celery_app inspect registered
```

---

## ✅ 验证结果

### 任务完成后的响应

```json
{
  "task_id": "test_001",
  "status": "completed",
  "progress": {
    "current_stage": "completed",
    "total_scenes": 3,
    "processed_scenes": 3,
    "percentage": 100
  },
  "result": {
    "video_url": "http://localhost:8003/videos/test_001.mp4",
    "duration": 45.2,
    "scenes": [
      {
        "scene_id": "scene_001",
        "text": "小明是一个活泼开朗的男孩。",
        "image_url": "/tmp/tfboys/images/test_001/scene_001.jpg",
        "audio_url": "/tmp/tfboys/audio/test_001/scene_001.mp3"
      }
    ]
  }
}
```

### 检查生成的文件

```bash
# 查看生成的图像
ls -la /tmp/tfboys/images/

# 查看生成的音频
ls -la /tmp/tfboys/audio/

# 查看生成的视频 (如果在本地)
ls -la /tmp/tfboys/videos/
```

---

## 🎯 测试完成标志

✅ **所有步骤完成的条件:**

1. ✅ API Service 响应 `200 OK`
2. ✅ Celery Worker 成功处理任务
3. ✅ 任务状态最终为 `completed`
4. ✅ 生成了图像、音频和视频文件
5. ✅ 无错误日志

**测试成功后，你将获得:**
- 分段的小说场景分析
- 每个场景的动漫风格图像
- 每个场景的中文配音
- 最终合成的视频（如果 Video Service 正常）

---

## 📝 下一步

测试成功后，你可以：
1. 尝试更长的文本输入
2. 测试不同的场景复杂度
3. 验证角色一致性维护
4. 集成到前端进行真实用户测试

