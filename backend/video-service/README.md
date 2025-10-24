# Video Service - TFBoys 视频合成服务

负责使用FFmpeg合成最终视频的服务。

## 主要功能

- 🎬 单场景视频合成 (图+音+字幕)
- 🔗 多场景视频拼接
- 📤 视频上传到OSS
- 🔄 回调通知

## 技术栈

- FastAPI
- FFmpeg
- Celery (异步任务)
- OSS (对象存储)

## 目录结构

```
app/
├── api/                      # API路由
│   └── internal.py          # 内部API
├── services/                 # 核心业务
│   ├── video_composer.py    # 视频合成主逻辑
│   ├── ffmpeg_executor.py   # FFmpeg执行器
│   └── subtitle_renderer.py # 字幕渲染
├── utils/
│   └── ffmpeg_builder.py    # FFmpeg命令构建
└── config.py
```

## 视频合成流程

```
接收场景数据
    ↓
下载图片和音频
    ↓
单场景合成 (图+音+字幕)
    ↓
多场景拼接
    ↓
上传到OSS
    ↓
回调AI服务
```

## FFmpeg关键命令

### 单场景合成

```bash
ffmpeg -loop 1 -i scene.jpg -i audio.mp3 \
  -vf "drawtext=text='字幕':fontfile=font.ttf" \
  -shortest scene.mp4
```

### 多场景拼接

```bash
ffmpeg -f concat -i scenes.txt -c copy final.mp4
```

## 开发

### 安装依赖

```bash
# 安装FFmpeg
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS

# 安装Python依赖
pip install -r requirements.txt
```

### 启动服务

```bash
# 启动API服务
uvicorn app.main:app --reload --port 8002

# 启动Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

## Docker部署

Dockerfile已包含FFmpeg安装。
