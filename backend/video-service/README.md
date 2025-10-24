# Video Service - TFBoys 视频合成服务

负责使用FFmpeg合成最终视频。

## 主要功能

- 🎬 **视频合成**: 使用FFmpeg合成图片、音频和字幕
- 📝 **字幕叠加**: 在视频上叠加字幕
- 🔗 **场景拼接**: 将多个场景合并为完整视频

## 技术栈

- FastAPI
- FFmpeg
- Celery + Redis
- 阿里云OSS

## 开发

```bash
# 安装FFmpeg
sudo apt-get install ffmpeg  # Linux
# brew install ffmpeg         # macOS

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002

# Celery Worker  
celery -A app.workers.celery_app worker --loglevel=info
```

## 环境变量

参见 `.env.example` 文件
