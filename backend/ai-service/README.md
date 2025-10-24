# AI Service - TFBoys AI处理服务

负责文本分析、图像生成和配音生成的核心AI服务。

## 主要功能

- 📝 **文本分析**: 使用GPT-4/Claude分析小说文本
- 🎨 **图像生成**: 调用Midjourney API生成动漫风格图像  
- 👤 **角色一致性**: 使用--cref参数保持角色视觉一致性
- 🎙️ **配音生成**: 调用阿里云TTS生成中文配音

## 开发

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

# Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

## 环境变量

参见 `.env.example` 文件
