# AI Service - TFBoys AI处理服务

负责文本分析、图像生成和配音生成的核心AI服务。

## 主要功能

- 📝 **文本分析**: 使用七牛 AI 推理 API (DeepSeek-V3) 分析小说文本，智能分割场景
- 🎨 **图像生成**: 使用七牛文生图 API (Gemini 2.5 Flash) 生成动漫风格图像
- 👤 **角色一致性**: 通过详细的提示词描述保持角色视觉一致性
- 🎙️ **配音生成**: 调用七牛 TTS 生成高质量中文配音

## 技术栈

- **AI 服务**: 七牛 AI Token API
  - 文本分析模型: `deepseek-v3`
  - 图像生成模型: `gemini-2.5-flash-image`
- **异步任务**: Celery + Redis
- **Web 框架**: FastAPI
- **存储**: 本地文件存储

## 开发

### 安装依赖

```bash
# 安装 shared 模块（在项目根目录执行）
pip install -e ./shared

# 安装服务依赖
cd backend/ai-service
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入七牛 API 密钥
```

### 启动服务

```bash
# 启动 API 服务
uvicorn app.main:app --reload --port 8001

# 启动 Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

### 运行测试

```bash
# 运行所有单元测试
python run_tests.py --unit

# 运行测试并生成覆盖率报告
python run_tests.py --unit --cov
```

## 环境变量

参见 `.env.example` 文件：

```bash
# 七牛 AI Token API 配置
QINIU_API_KEY=your-qiniu-ai-token-api-key

# 七牛 TTS 服务配置
QINIU_ACCESS_KEY=your-qiniu-access-key
QINIU_SECRET_KEY=your-qiniu-secret-key

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# Video Service URL
VIDEO_SERVICE_URL=http://localhost:8002
```

## API 文档

启动服务后访问:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
