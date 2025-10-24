# TFBoys 项目开发指南

本文档为 AI 辅助开发工具(如 Claude Code、GitHub Copilot)提供项目结构和开发规范说明。

## 📋 项目概述

**项目名称**: TFBoys (Token Free Boys)  
**描述**: 基于大模型的小说文字转动漫视频系统  
**架构**: Monorepo (前后端代码在同一仓库)

### 技术栈

**前端**:
- React + TypeScript
- Vite
- Ant Design
- Axios

**后端**:
- Python 3.11+
- FastAPI
- Celery + Redis (异步任务队列)
- OpenAI GPT-4 / Anthropic Claude (文本分析)
- Midjourney API (图像生成)
- 阿里云 TTS (配音生成)
- FFmpeg (视频合成)
- 阿里云 OSS (对象存储)

### 服务架构

```
┌─────────────────┐
│   Frontend      │ (React, Port 3000)
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  API Gateway    │ (FastAPI, Port 8000)
└─────┬───────────┘
      │
      ├──────────► AI Service (FastAPI, Port 8001)
      │              - 文本分析
      │              - 图像生成
      │              - 配音生成
      │
      └──────────► Video Service (FastAPI, Port 8002)
                     - 视频合成
                     - FFmpeg 处理
```

---

## 📁 目录结构规范

### 根目录结构

```
tfboys/
├── frontend/              # 前端应用
├── backend/               # 后端服务
│   ├── api-gateway/      # API 网关
│   ├── ai-service/       # AI 处理服务
│   └── video-service/    # 视频合成服务
├── shared/                # 共享代码
│   ├── models/           # 跨服务共享数据模型
│   ├── clients/          # 共享客户端(OSS、Redis)
│   ├── constants.py      # 常量定义
│   ├── enums.py          # 枚举类型
│   └── exceptions.py     # 自定义异常
├── docs/                  # 文档
├── scripts/               # 工具脚本
└── docker/                # Docker 配置
```

### 后端服务统一结构

每个后端服务(api-gateway、ai-service、video-service)遵循相同的目录结构:

```
backend/<service-name>/
├── app/
│   ├── main.py           # FastAPI 应用入口
│   ├── config.py         # 配置管理(Pydantic Settings)
│   ├── api/              # API 路由层
│   ├── models/           # 服务特定数据模型
│   ├── services/         # 业务逻辑层
│   ├── workers/          # Celery 异步任务(如果需要)
│   └── utils/            # 服务特定工具函数
├── tests/                # 测试
├── requirements.txt      # Python 依赖
├── Dockerfile            # Docker 镜像
└── .env.example          # 环境变量模板
```

### shared/ 目录组织

**何时放到 shared/**:
- ✅ 被 **2个及以上服务** 使用的代码
- ✅ 跨服务共享的数据模型(如 Scene、Character、Task)
- ✅ 通用客户端(OSS、Redis)
- ✅ 常量、枚举、异常定义

**不应该放到 shared/**:
- ❌ 仅被单个服务使用的代码
- ❌ 服务特定的业务逻辑

### services/ vs utils/ 的区别

**services/ - 业务逻辑层**:
- 包含业务逻辑
- 调用外部 API 或服务
- 例如: `text_analyzer.py` (调用 GPT-4)、`image_generator.py` (调用 Midjourney)、`video_client.py` (调用 Video Service)

**utils/ - 工具函数层**:
- 纯工具函数,无业务逻辑
- 可复用的通用函数
- 例如: `prompt_builder.py` (构建 Prompt)、`retry.py` (重试装饰器)、`logger.py` (日志配置)

---

## 💻 代码规范

### Python 代码规范

#### 格式化工具
- **Black**: 代码格式化
- **isort**: import 排序
- **mypy**: 类型检查(可选)

#### 类型注解
所有函数必须有类型注解:

```python
from typing import List, Optional

async def analyze_novel(novel_text: str) -> List[Scene]:
    """分析小说文本"""
    pass

def get_task_status(task_id: str) -> Optional[Task]:
    """获取任务状态"""
    pass
```

#### 命名规范
- **文件名**: `snake_case.py` (例如: `text_analyzer.py`)
- **类名**: `PascalCase` (例如: `TextAnalyzer`)
- **函数名**: `snake_case` (例如: `analyze_novel()`)
- **常量**: `UPPER_SNAKE_CASE` (例如: `MAX_RETRIES = 3`)
- **私有函数**: `_function_name()` (前缀下划线)

#### 导入顺序
```python
# 1. 标准库
import os
import sys
from typing import List

# 2. 第三方库
from fastapi import FastAPI
from pydantic import BaseModel

# 3. 本地导入
from app.config import settings
from shared.models.scene import Scene
```

### TypeScript 代码规范

#### 格式化工具
- **ESLint**: 代码检查
- **Prettier**: 代码格式化

#### 命名规范
- **文件名**: `camelCase.ts` 或 `PascalCase.tsx` (组件)
- **接口/类型**: `PascalCase` (例如: `Task`, `Scene`)
- **函数**: `camelCase` (例如: `createTask()`)
- **常量**: `UPPER_SNAKE_CASE` (例如: `API_BASE_URL`)

---

## 🔄 开发工作流

### Git 分支策略

- **main**: 主分支,受保护,仅通过 PR 合并
- **feature/<name>**: 功能分支 (例如: `feature/text-analysis`)
- **fix/<name>**: Bug 修复分支 (例如: `fix/audio-sync`)
- **docs/<name>**: 文档分支 (例如: `docs/api-guide`)

### 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**:
```
feat(ai-service): 实现角色一致性管理

- 添加 CharacterManager 类
- 实现角色库 Redis 存储
- 支持 Midjourney --cref 参数

Closes #10
```

### Pull Request 规范

**PR 标题**: 与提交信息格式相同  
**PR 描述**:
```markdown
## 变更内容
- 变更点1
- 变更点2

## 测试
- [ ] 单元测试通过
- [ ] 手动测试通过

## 相关 Issue
Closes #10
```

---

## 🚀 常用命令

### 启动所有服务(开发环境)

```bash
# 方式1: Docker Compose(推荐)
make up

# 方式2: 本地启动
# 终端1: API Gateway
cd backend/api-gateway && uvicorn app.main:app --reload --port 8000

# 终端2: AI Service
cd backend/ai-service && uvicorn app.main:app --reload --port 8001

# 终端3: Video Service
cd backend/video-service && uvicorn app.main:app --reload --port 8002

# 终端4: Celery Worker (AI Service)
cd backend/ai-service && celery -A app.workers.celery_app worker --loglevel=info

# 终端5: Celery Worker (Video Service)
cd backend/video-service && celery -A app.workers.celery_app worker --loglevel=info

# 终端6: 前端
cd frontend && npm run dev
```

### 测试

```bash
# 运行所有测试
make test

# 单个服务测试
cd backend/ai-service && pytest

# 测试覆盖率
cd backend/ai-service && pytest --cov=app --cov-report=html
```

### 代码检查

```bash
# Python
cd backend/ai-service
black app/
isort app/
mypy app/

# TypeScript
cd frontend
npm run lint
npm run format
```

---

## 🔐 环境变量管理

### AI Service (.env)

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY=sk-xxx

# Anthropic
ANTHROPIC_API_KEY=sk-ant-xxx

# Midjourney
MIDJOURNEY_API_KEY=xxx
MIDJOURNEY_API_URL=https://api.midjourney.com/v1

# 阿里云 TTS
ALIYUN_TTS_ACCESS_KEY=xxx
ALIYUN_TTS_SECRET_KEY=xxx
ALIYUN_TTS_APP_KEY=xxx

# 阿里云 OSS
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_ACCESS_KEY=xxx
OSS_SECRET_KEY=xxx
OSS_BUCKET=tfboys

# Video Service URL
VIDEO_SERVICE_URL=http://localhost:8002
```

### Video Service (.env)

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# 阿里云 OSS
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_ACCESS_KEY=xxx
OSS_SECRET_KEY=xxx
OSS_BUCKET=tfboys
```

### 环境变量使用

- ✅ 使用 `.env` 文件存储本地配置(不提交到 Git)
- ✅ 提供 `.env.example` 作为模板(提交到 Git)
- ✅ 使用 `pydantic-settings` 管理配置

---

## 🎯 核心业务逻辑

### 完整数据流程

```
1. 用户上传小说 → Frontend
   ↓
2. Frontend → POST /tasks → API Gateway
   ↓
3. API Gateway → POST /internal/tasks → AI Service
   ↓
4. AI Service 触发 Celery 任务:
   4.1 文本分析(GPT-4/Claude)
       → 场景分割
       → 角色提取
   
   4.2 角色管理
       → 为每个角色生成设定图(Midjourney)
       → 保存到 OSS
       → 保存角色信息到 Redis
   
   4.3 场景图像生成
       → 使用 Midjourney + --cref 生成场景图
       → 保存到 OSS
   
   4.4 配音生成
       → 使用阿里云 TTS 生成配音
       → 保存到 OSS
   
   4.5 提交到 Video Service
       → POST /internal/video-synthesis/jobs
   ↓
5. Video Service:
   5.1 下载图片和音频
   5.2 使用 FFmpeg 合成视频
   5.3 上传视频到 OSS
   5.4 回调 AI Service
       → POST /callbacks/video-completed
   ↓
6. AI Service 更新任务状态到 Redis
   ↓
7. Frontend 轮询任务状态
   → GET /tasks/{task_id}
   → 显示视频下载链接
```

### 角色一致性实现

**核心技术**: Midjourney 的 `--cref` (Character Reference) 参数

**实现步骤**:
1. 首次遇到角色时,生成角色设定图:
   ```
   prompt: "anime style, [角色描述], character design --niji 6"
   ```

2. 保存角色图到 OSS:
   ```
   路径: characters/{character_id}.jpg
   ```

3. 保存角色信息到 Redis:
   ```python
   {
     "character_id": "char_001",
     "name": "主角",
     "reference_image_url": "https://oss.../characters/char_001.jpg"
   }
   ```

4. 后续场景使用 `--cref` 参数:
   ```
   prompt: "[场景描述] --niji 6 --ar 16:9 --cref https://oss.../characters/char_001.jpg --cw 100"
   ```

**参数说明**:
- `--cref <URL>`: 角色参考图 URL
- `--cw <0-100>`: Character Weight,推荐值 100(完全一致)

### Redis Key 命名规范

```python
# 任务状态
task:{task_id}
TTL: 7天

# 角色库
character:{character_id}
TTL: 永久

# 任务的角色列表
task:{task_id}:characters
TTL: 7天
```

### OSS 路径规范

```
bucket/
├── characters/          # 角色设定图
│   ├── char_001.jpg
│   └── char_002.jpg
├── scenes/              # 场景图片
│   └── {task_id}/
│       ├── scene_001.jpg
│       └── scene_002.jpg
├── audio/               # 配音文件
│   └── {task_id}/
│       ├── scene_001.mp3
│       └── scene_002.mp3
├── videos/              # 最终视频
│   └── {task_id}.mp4
└── thumbnails/          # 视频缩略图
    └── {task_id}.jpg
```

---

## 🧪 测试策略

### 单元测试

**要求**: 覆盖率 ≥ 80%

**示例**:
```python
# tests/unit/test_text_analyzer.py
import pytest
from app.services.text_analyzer import TextAnalyzer

@pytest.mark.asyncio
async def test_analyze_novel():
    analyzer = TextAnalyzer()
    scenes = await analyzer.analyze_novel("测试小说文本...")
    
    assert len(scenes) > 0
    assert scenes[0].description is not None
    assert scenes[0].characters is not None

@pytest.mark.asyncio
async def test_extract_characters():
    analyzer = TextAnalyzer()
    characters = await analyzer.extract_characters("小说文本...")
    
    assert len(characters) > 0
    assert characters[0].name is not None
```

### 集成测试

**示例**:
```python
# tests/integration/test_workflow.py
import pytest
from app.workers.tasks import process_video_generation

@pytest.mark.asyncio
async def test_full_workflow():
    task_id = "test_task_001"
    novel_text = "这是一个测试小说..."
    
    result = await process_video_generation(task_id, novel_text)
    
    assert result["status"] == "completed"
    assert result["video_url"] is not None
```

### Mock 数据

开发阶段使用 Mock 数据避免调用真实 API:

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_openai_client(monkeypatch):
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = MockResponse(
        choices=[{"message": {"content": '{"scenes": [...]}'}}]
    )
    monkeypatch.setattr("app.services.text_analyzer.OpenAI", lambda **kwargs: mock_client)
    return mock_client
```

---

## ⚠️ 错误处理

### 自定义异常

使用 `shared/exceptions.py` 中定义的异常:

```python
from shared.exceptions import AIServiceException

class TextAnalysisError(AIServiceException):
    """文本分析失败"""
    pass

class ImageGenerationError(AIServiceException):
    """图像生成失败"""
    pass
```

### HTTP 错误码

```python
from fastapi import HTTPException

# 400 Bad Request
raise HTTPException(status_code=400, detail="小说文本不能为空")

# 404 Not Found
raise HTTPException(status_code=404, detail="任务不存在")

# 500 Internal Server Error
raise HTTPException(status_code=500, detail="服务器内部错误")
```

### 重试机制

使用 `tenacity` 库处理 API 限流:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_midjourney_api(prompt: str) -> str:
    """调用 Midjourney API,失败自动重试"""
    response = await client.post("/imagine", json={"prompt": prompt})
    return response.json()["image_url"]
```

---

## 🔒 安全注意事项

### API 密钥管理

- ✅ 使用环境变量存储 API 密钥
- ✅ 不要将 `.env` 文件提交到 Git
- ✅ 使用 `.env.example` 提供模板
- ❌ 不要在代码中硬编码密钥

### 用户输入验证

```python
from pydantic import BaseModel, validator

class TaskCreateRequest(BaseModel):
    novel_text: str
    
    @validator('novel_text')
    def validate_novel_text(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('小说文本不能为空')
        if len(v) > 100000:
            raise ValueError('小说文本过长(最大100000字符)')
        return v
```

### OSS 文件权限

- ✅ 角色图、场景图、音频、视频设置为 **公开读**
- ✅ 使用签名 URL 访问敏感文件(如果需要)
- ❌ 不要将用户上传的原始文件直接存储

---

## ❓ 常见问题

### Q1: 如何添加新的 AI 模型(如 Claude)?

**A**: 在 `text_analyzer.py` 中添加:

```python
from anthropic import Anthropic

class TextAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
    
    async def analyze_novel_with_claude(self, novel_text: str):
        response = await self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content
```

### Q2: 如何调整视频质量?

**A**: 修改 Video Service 的 FFmpeg 参数:

```python
# app/services/ffmpeg_executor.py
ffmpeg_cmd = [
    "ffmpeg",
    "-i", "input.mp4",
    "-c:v", "libx264",
    "-preset", "medium",     # 修改为 slow 提升质量
    "-crf", "23",            # 修改为 18-20 提升质量(越小越好)
    "-c:a", "aac",
    "-b:a", "192k",          # 修改为 256k 提升音质
    "output.mp4"
]
```

### Q3: 如何扩展角色一致性算法?

**A**: 在 `character_manager.py` 中实现:

```python
async def get_character_refs_for_scene(self, scene: Scene) -> Dict[str, str]:
    """获取场景中所有角色的参考图"""
    refs = {}
    for character in scene.characters:
        ref_url = await self.get_character_ref(character.character_id)
        if ref_url:
            refs[character.character_id] = ref_url
    return refs
```

### Q4: 如何添加新的配音音色?

**A**: 在 `voice_generator.py` 中添加:

```python
VOICE_TYPES = {
    "female": "xiaoyun",     # 阿里云 TTS 音色 ID
    "male": "xiaogang",
    "child": "aixia",        # 新增音色
}

async def generate_voice(self, text: str, voice_type: str = "female"):
    voice_id = VOICE_TYPES.get(voice_type, "xiaoyun")
    # 调用阿里云 TTS API
```

---

## 📚 相关文档

- [技术方案设计](./DESIGN.md)
- [系统架构设计](./ARCHITECTURE.md)
- [API 接口文档](./API.md)
- [代码目录结构](./DIRECTORY_STRUCTURE.md)

---

## 🚀 部署说明

### Docker Compose 部署

```bash
# 1. 配置环境变量
cp backend/ai-service/.env.example backend/ai-service/.env
cp backend/video-service/.env.example backend/video-service/.env
# 编辑 .env 文件,填入真实的 API 密钥

# 2. 构建镜像
make build

# 3. 启动所有服务
make up

# 4. 查看日志
make logs

# 5. 停止服务
make down
```

### 生产环境部署

- 使用 Nginx 作为反向代理
- 使用 Supervisor 管理 Celery Worker
- 使用 Redis Cluster 提升性能
- 使用 CDN 加速 OSS 资源访问
- 启用 HTTPS
- 配置日志收集(ELK Stack)
- 配置监控告警(Prometheus + Grafana)

---

**最后更新**: 2025-10-24  
**维护者**: TFBoys 团队
