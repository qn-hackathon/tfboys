# TFBoys - AI 辅助开发指南

本文档为 AI 助手(Claude Code、GitHub Copilot 等)提供项目结构、开发规范和核心业务逻辑说明。

## 📋 项目概述

**项目名称**: TFBoys - 文字生成视频系统

**技术栈**:
- 后端: Python 3.10+ (FastAPI, Celery)
- 前端: React + TypeScript
- 数据库: Redis
- 消息队列: Celery + Redis
- 文件存储: 本地文件系统 (/tmp/tfboys)
- AI 服务: OpenAI GPT-4/Claude, DALL-E 3, 七牛云 TTS

**架构**: Monorepo (所有服务在一个仓库中)

**后端服务**:
1. API Gateway (端口 8001) - 用户请求入口
2. AI Service (端口 8002) - AI 处理服务
3. Video Service (端口 8003) - 视频合成服务

---

## 📁 目录结构规范

### 1. Shared 模块 (跨服务共享)

```
shared/
├── models/          # 共享数据模型
│   ├── scene.py     # Scene + Character 模型
│   └── task.py      # Task 模型
├── clients/         # 共享客户端
│   ├── local_storage_client.py  # 本地文件存储客户端
│   └── redis_client.py    # Redis 客户端
├── constants.py     # 常量定义
├── enums.py         # 枚举类型
└── exceptions.py    # 自定义异常
```

### 2. 后端服务统一结构

```
backend/<service-name>/
├── app/
│   ├── api/         # API 路由层
│   ├── models/      # 服务特有的数据模型
│   ├── services/    # 业务逻辑层
│   ├── utils/       # 服务特有的工具函数
│   ├── schemas/     # API 请求/响应 Schema
│   ├── config.py    # 配置管理
│   └── main.py      # FastAPI 应用入口
├── requirements.txt
└── Dockerfile
```

### 3. services/ vs utils/ 的区别

**services/** (业务逻辑层):
- 调用外部服务的客户端 (GPT-4, DALL-E 3, Video Service)
- 包含业务逻辑的服务类
- 示例: `text_analyzer.py`, `image_generator.py`, `video_client.py`

**utils/** (纯工具函数):
- 不包含业务逻辑的辅助函数
- 可重用的通用工具
- 示例: `retry.py`, `logger.py`, `prompt_builder.py`

### 4. 何时放到 shared/

**判断标准**: 如果一个模块被 **2个及以上服务** 使用,就应该放到 `shared/`

**示例**:
- `Scene` 模型 → API Gateway、AI Service、Video Service 都使用 → 放到 `shared/models/`
- `RedisClient` → API Gateway、AI Service 都使用 → 放到 `shared/clients/`
- `PromptBuilder` → 仅 AI Service 使用 → 放到 `ai-service/app/utils/`

---

## 💻 代码规范

### 语言规范

**重要**: 本项目强制使用中文作为主要语言

1. **代码注释**: 所有注释必须使用中文
2. **文档字符串**: 所有 docstring 必须使用中文
3. **变量命名**: 使用英文命名,但相关注释必须是中文
4. **提交信息**: Git commit message 必须使用中文
5. **Pull Request**: PR 标题和描述必须使用中文
6. **文档**: 所有 Markdown 文档(.md)必须使用中文
7. **专有名词例外**: 以下技术术语可保留英文:
   - API 名称 (如 OpenAI API, Claude API, DALL-E 3)
   - 框架名称 (如 FastAPI, React, Redis)
   - 技术术语 (如 HTTP, REST, JSON, Docker)
   - 第三方服务名称 (如 GitHub, Celery)
   - 代码中的关键字和标准库名称

**示例**:
```python
# ✅ 正确: 使用中文注释
async def generate_image(scene_desc: str) -> str:
    """
    生成场景图像
    
    Args:
        scene_desc: 场景描述
        
    Returns:
        str: 生成的图像 URL
    """
    # 调用 DALL-E 3 API 生成图像
    response = await openai_client.create_image(scene_desc)
    return response.url

# ❌ 错误: 使用英文注释
async def generate_image(scene_desc: str) -> str:
    """
    Generate scene image
    
    Args:
        scene_desc: Scene description
        
    Returns:
        str: Generated image URL
    """
    # Call DALL-E 3 API to generate image
    response = await openai_client.create_image(scene_desc)
    return response.url
```

**提交信息示例**:
```
✅ 正确:
feat(ai-service): 添加角色一致性支持
fix(api-gateway): 修复任务创建超时问题
docs(readme): 更新安装指南

❌ 错误:
feat(ai-service): add character consistency support
fix(api-gateway): resolve task creation timeout
docs(readme): update installation guide
```

### Python 代码规范

1. **代码格式化**: 使用 Black (line-length=100)
2. **导入排序**: 使用 isort
3. **类型注解**: 所有函数必须有类型注解
4. **文档字符串**: 使用 Google 风格的 docstring (中文)

```python
async def generate_image(scene_desc: str, character_refs: List[str]) -> str:
    """
    生成场景图像
    
    Args:
        scene_desc: 场景描述
        character_refs: 角色参考图 URL 列表
        
    Returns:
        str: 生成的图像 URL
        
    Raises:
        ImageGenerationException: 图像生成失败
    """
    pass
```

### TypeScript 代码规范

1. **代码格式化**: 使用 Prettier
2. **代码检查**: 使用 ESLint
3. **类型定义**: 所有变量和函数必须有类型定义

### 命名规范

- **文件名**: snake_case (Python: `text_analyzer.py`, TypeScript: `task-list.tsx`)
- **类名**: PascalCase (`class TextAnalyzer`)
- **函数名**: snake_case (`def analyze_novel()`)
- **常量**: UPPER_SNAKE_CASE (`MAX_RETRIES = 3`)

### 导入顺序

```python
# 1. 标准库
import os
import json

# 2. 第三方库
from fastapi import APIRouter
from pydantic import BaseModel

# 3. 共享模块
from shared.models import Scene, Character
from shared.clients import redis_client

# 4. 本地模块
from app.config import settings
from app.services.text_analyzer import TextAnalyzer
```

---

## 🔄 开发工作流

### Git 分支策略

- `main`: 主分支,保护分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支

### 提交信息规范

使用 Conventional Commits:

```
feat(ai-service): add character consistency support
fix(api-gateway): resolve task creation timeout
docs(readme): update installation guide
refactor(shared): move redis client to shared
```

### Pull Request 规范

1. PR 标题使用 Conventional Commits 格式
2. PR 描述包含:
   - 变更内容摘要
   - 测试方法
   - 相关 Issue 链接

---

## 🚀 常用命令

### 启动所有后端服务

```bash
# API Gateway
cd backend/api-gateway && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# AI Service
cd backend/ai-service && uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

# Video Service
cd backend/video-service && uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

### 启动 Celery Worker (AI Service)

```bash
cd backend/ai-service
celery -A app.workers.celery_app worker --loglevel=info
```

### 测试

```bash
# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 运行所有测试并生成覆盖率报告
pytest --cov=app --cov-report=html
```

### 代码检查

```bash
# Python
black . --check
isort . --check
flake8 .

# TypeScript
npm run lint
npm run type-check
```

---

## 🔐 环境变量管理

### AI Service 环境变量

创建 `backend/ai-service/.env`:

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# Video Service
VIDEO_SERVICE_URL=http://localhost:8003

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=...

# DALL-E 3 (使用 OpenAI API)
# DALL-E 3 图像生成通过 OPENAI_API_KEY 实现，无需额外配置

# 七牛云 TTS
QINIU_ACCESS_KEY=...
QINIU_SECRET_KEY=...

# 阿里云 OSS




```

### Video Service 环境变量

创建 `backend/video-service/.env`:

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# 阿里云 OSS





# AI Service (用于回调)
AI_SERVICE_URL=http://localhost:8002
```

### .env vs .env.example

- `.env`: 真实环境变量,**不提交到 Git**
- `.env.example`: 环境变量模板,提交到 Git

---

## 🎯 核心业务逻辑

### 完整数据流程

```
1. 用户提交小说文本 → API Gateway
   ↓
2. API Gateway → AI Service (创建任务)
   ↓
3. AI Service 异步处理:
   ├─ 3.1 文本分析 (GPT-4) → 生成场景列表
   ├─ 3.2 提取角色 → 保存到 Redis 角色库
   ├─ 3.3 生成角色设定图 (DALL-E 3)
   ├─ 3.4 生成场景图像 (DALL-E 3 + --cref)
   ├─ 3.5 生成配音 (七牛云 TTS)
   └─ 3.6 提交到 Video Service
   ↓
4. Video Service 合成视频 (FFmpeg)
   ↓
5. Video Service 回调 AI Service → 更新任务状态
   ↓
6. 用户查询任务状态 → API Gateway → Redis
```

### 角色一致性实现 (DALL-E 3)

**核心原理**: 使用 DALL-E 3 通过详细的角色描述提示词来保持角色一致性

**注意**: DALL-E 3 不支持图像引用参数（如 DALL-E 3 的 --cref），因此我们通过在每个场景的提示词中包含详细的角色特征描述来维持一致性。

**步骤**:

1. **首次生成角色设定图**:
```python
prompt = "Anime style character design sheet for 小明. Short black hair, blue eyes, white background, character sheet style, high quality anime illustration."
character_image_url = await image_generator.generate_character_image(
    character_name="小明",
    character_description="short black hair, blue eyes"
)
```

2. **保存角色到 Redis**:
```python
await redis_client.save_character("char_001", {
    "name": "小明",
    "description": "short black hair, blue eyes",
    "reference_image_url": character_image_url
})
```

3. **生成场景图像时使用详细角色描述**:
```python
character_ref = await redis_client.get_character("char_001")
prompt = f"Anime style scene. 小明 ({character_ref['description']}) standing in a park, sunny day. Cinematic composition, high quality anime illustration."
scene_image_url = await image_generator.generate_scene_image(
    scene_description="小明 standing in a park, sunny day",
    scene_id="scene_001",
    character_context=f"{character_ref['name']}: {character_ref['description']}"
)
```

**关键策略**:
- 在每个提示词中包含完整的角色特征描述
- 保持角色描述的一致性和详细性
- 使用统一的艺术风格提示（"Anime style", "high quality anime illustration"）

### Redis Key 命名规范

```
task:{task_id}                    # 任务数据 (TTL: 7天)
task:{task_id}:characters         # 任务的角色ID列表 (Set)
character:{character_id}          # 角色数据 (永久)
tasks                             # 所有任务ID集合 (Set)
```

### OSS 路径规范

```
characters/{character_id}.jpg        # 角色设定图
scenes/{task_id}/{scene_id}.jpg      # 场景图像
audio/{task_id}/{scene_id}.mp3       # 配音文件
videos/{task_id}/final.mp4           # 最终视频
```

---

## 🧪 测试策略

### 单元测试要求

- 覆盖率 ≥ 80%
- 所有核心业务逻辑必须有单元测试
- 使用 Mock 隔离外部依赖

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_analyze_novel():
    """测试文本分析"""
    analyzer = TextAnalyzer()
    
    with patch('openai.ChatCompletion.acreate') as mock_openai:
        mock_openai.return_value = AsyncMock(choices=[...])
        
        scenes = await analyzer.analyze_novel("测试小说...")
        
        assert len(scenes) > 0
        assert scenes[0].description is not None
```

### 集成测试

```python
@pytest.mark.asyncio
async def test_full_workflow():
    """测试完整工作流"""
    task_id = "test_task_001"
    novel_text = "测试小说..."
    
    # 1. 创建任务
    response = await client.post("/internal/tasks", json={
        "task_id": task_id,
        "novel_text": novel_text
    })
    assert response.status_code == 200
    
    # 2. 等待处理完成
    await asyncio.sleep(10)
    
    # 3. 检查任务状态
    task_data = await redis_client.get_task(task_id)
    assert task_data["status"] == "completed"
```

---

## ⚠️ 错误处理

### 自定义异常

```python
from shared.exceptions import (
    TextAnalysisException,
    ImageGenerationException,
    VoiceGenerationException
)

try:
    scenes = await text_analyzer.analyze_novel(novel_text)
except Exception as e:
    raise TextAnalysisException(str(e))
```

### HTTP 错误码

- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `404`: 资源未找到
- `500`: 服务器内部错误
- `503`: 外部服务不可用

### 重试机制

```python
from app.utils.retry import retry_on_failure

@retry_on_failure(max_retries=3, delay=2.0, backoff=2.0)
async def call_external_api():
    response = await httpx.get("https://api.example.com")
    return response.json()
```

---

## 🔒 安全注意事项

1. **API 密钥管理**:
   - 所有密钥通过环境变量注入
   - 不在代码中硬编码密钥
   - 不提交 `.env` 文件到 Git

2. **用户输入验证**:
   - 所有用户输入必须验证
   - 使用 Pydantic 模型验证请求参数
   - 防止 SQL 注入和 XSS 攻击

3. **OSS 文件权限**:
   - 角色设定图和场景图像设置为公开读
   - 最终视频文件设置签名 URL (24小时有效)

---

## ❓ 常见问题

### 1. 如何添加新的 AI 模型?

1. 在 `backend/ai-service/app/services/` 创建新的服务类
2. 在 `app/config.py` 添加相关配置
3. 在 `app/workers/tasks.py` 中集成到工作流

### 2. 如何调整视频质量?

修改 `backend/video-service/app/services/video_composer.py` 中的 FFmpeg 参数:

```python
ffmpeg_command = [
    'ffmpeg',
    '-i', 'input.mp4',
    '-vcodec', 'libx264',
    '-crf', '18',  # 质量参数 (0-51, 越小质量越高)
    '-preset', 'slow',  # slow = 高质量
    'output.mp4'
]
```

### 3. 如何扩展角色一致性算法?

当前使用 DALL-E 3 的详细提示词策略，如需更高级的一致性:

1. 考虑使用 Stable Diffusion + ControlNet (支持图像引用)
2. 使用专业的角色一致性模型 (如 InsightFace)
3. 考虑 DALL-E 3 API 代理服务 (支持 --cref 参数)
4. 在 `app/services/character_manager.py` 中实现新算法

### 4. 如何添加新的配音音色?

1. 在 `shared/enums.py` 中添加新的 `TTSVoice` 枚举值
2. 在 `backend/ai-service/app/services/voice_generator.py` 中映射到七牛云 TTS 的音色 ID

---

## 🚀 部署说明

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f ai-service
```

### 生产环境配置

1. 使用环境变量注入敏感信息
2. 启用 HTTPS
3. 配置 Nginx 反向代理
4. 配置 Redis 持久化
5. 配置 Celery Worker 监控 (Flower)

---

## 📚 参考文档

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Celery 文档](https://docs.celeryproject.org/)
- [OpenAI DALL-E 3 文档](https://platform.openai.com/docs/guides/images)
- [阿里云 OSS 文档](https://help.aliyun.com/product/31815.html)
- [七牛云 TTS 文档](https://developer.qiniu.com/dora/8091/speech-synthesis)

---

**最后更新**: 2024-10-24
**维护者**: TFBoys Team
