# AI Service - TFBoys AI处理服务

负责文本分析、图像生成和配音生成的核心AI服务。

## 主要功能

- 📝 文本分析 (GPT-4/Claude)
- 🎨 图像生成 (Midjourney API)
- 🎤 配音生成 (阿里云TTS)
- 👤 角色一致性管理

## 技术栈

- FastAPI
- Celery (异步任务)
- OpenAI SDK
- Anthropic SDK
- Midjourney API
- 阿里云TTS

## 目录结构

```
app/
├── api/                        # API路由
│   ├── internal.py            # 内部API
│   └── callbacks.py           # 回调接口
├── services/                   # 核心业务
│   ├── text_analyzer.py       # 文本分析
│   ├── image_generator.py     # 图像生成(Midjourney)
│   ├── voice_generator.py     # 配音生成(TTS)
│   └── character_manager.py   # 角色管理
├── workers/                    # Celery任务
│   ├── celery_app.py
│   └── tasks.py
└── config.py
```

## 核心流程

```
小说文本输入
    ↓
文本分析(GPT-4) → 场景分割 + 角色识别
    ↓
图像生成(Midjourney + --cref)
    ↓
配音生成(阿里云TTS)
    ↓
发送场景数据到视频服务
```

## 角色一致性实现

使用Midjourney的`--cref`参数:

1. 首次出现角色 → 生成角色设定图
2. 保存到角色库 (Redis)
3. 后续场景 → 使用`--cref <角色图URL>`

## 开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
cp .env.example .env
# 填入API密钥
```

### 启动服务

```bash
# 启动API服务
uvicorn app.main:app --reload --port 8001

# 启动Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

## API密钥配置

需要配置以下API密钥:

- OpenAI API Key
- Midjourney API Key
- 阿里云TTS密钥
- OSS存储密钥
