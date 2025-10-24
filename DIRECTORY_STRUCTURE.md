# 代码目录结构设计

## 总体说明

本项目采用 **Monorepo** 架构,前后端代码在同一个仓库中,通过根目录层级区分。

```
tfboys/                           # 项目根目录
├── frontend/                     # 前端模块(React/Vue)
├── backend/                      # 后端模块
│   ├── api-gateway/             # API网关服务
│   ├── ai-service/              # AI处理服务
│   └── video-service/           # 视频合成服务
├── shared/                       # 共享代码/工具
├── docs/                         # 项目文档
├── scripts/                      # 脚本工具
└── docker/                       # Docker配置
```

---

## 完整目录结构

```
tfboys/
│
├── README.md                     # 项目总览
├── DESIGN.md                     # 技术方案设计
├── ARCHITECTURE.md               # 架构设计文档
├── API.md                        # API接口定义
├── DIRECTORY_STRUCTURE.md        # 本文档
├── .gitignore                    # Git忽略规则
├── docker-compose.yml            # Docker编排配置
├── Makefile                      # 快捷命令
│
├── frontend/                     # 【前端模块】
│   ├── package.json              # 前端依赖
│   ├── tsconfig.json             # TypeScript配置
│   ├── vite.config.ts            # Vite构建配置(或webpack.config.js)
│   ├── .env.development          # 开发环境变量
│   ├── .env.production           # 生产环境变量
│   │
│   ├── public/                   # 静态资源
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/               # 图片/字体等
│   │
│   ├── src/                      # 源代码
│   │   ├── main.tsx              # 入口文件
│   │   ├── App.tsx               # 根组件
│   │   │
│   │   ├── pages/                # 页面组件
│   │   │   ├── Home/             # 首页
│   │   │   │   ├── index.tsx
│   │   │   │   └── styles.css
│   │   │   ├── TaskCreate/       # 任务创建页
│   │   │   ├── TaskList/         # 任务列表页
│   │   │   └── VideoPreview/     # 视频预览页
│   │   │
│   │   ├── components/           # 公共组件
│   │   │   ├── Header/
│   │   │   ├── Footer/
│   │   │   ├── UploadArea/       # 文本上传组件
│   │   │   ├── TaskCard/         # 任务卡片
│   │   │   └── ProgressBar/      # 进度条
│   │   │
│   │   ├── services/             # API服务层
│   │   │   ├── api.ts            # Axios实例配置
│   │   │   ├── taskService.ts    # 任务相关API
│   │   │   └── videoService.ts   # 视频相关API
│   │   │
│   │   ├── hooks/                # 自定义Hooks
│   │   │   ├── useTask.ts        # 任务状态Hook
│   │   │   └── usePolling.ts     # 轮询Hook
│   │   │
│   │   ├── store/                # 状态管理(Redux/Zustand)
│   │   │   ├── index.ts
│   │   │   └── taskSlice.ts
│   │   │
│   │   ├── types/                # TypeScript类型定义
│   │   │   ├── task.ts
│   │   │   └── api.ts
│   │   │
│   │   └── utils/                # 工具函数
│   │       ├── format.ts         # 格式化
│   │       └── validator.ts      # 验证
│   │
│   └── tests/                    # 前端测试
│       └── unit/
│
├── backend/                      # 【后端模块】
│   │
│   ├── api-gateway/              # 【API网关服务】
│   │   ├── requirements.txt      # Python依赖
│   │   ├── Dockerfile            # Docker镜像
│   │   ├── .env.example          # 环境变量示例
│   │   │
│   │   ├── app/                  # 应用代码
│   │   │   ├── main.py           # FastAPI入口
│   │   │   ├── config.py         # 配置管理
│   │   │   │
│   │   │   ├── api/              # API路由
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tasks.py      # 任务相关路由
│   │   │   │   └── health.py     # 健康检查
│   │   │   │
│   │   │   ├── models/           # 数据模型
│   │   │   │   ├── __init__.py
│   │   │   │   ├── task.py
│   │   │   │   └── response.py
│   │   │   │
│   │   │   ├── services/         # 业务逻辑
│   │   │   │   ├── __init__.py
│   │   │   │   ├── task_service.py
│   │   │   │   └── redis_client.py
│   │   │   │
│   │   │   └── middleware/       # 中间件
│   │   │       ├── __init__.py
│   │   │       ├── cors.py
│   │   │       └── logging.py
│   │   │
│   │   └── tests/                # 测试
│   │       ├── test_api.py
│   │       └── conftest.py
│   │
│   ├── ai-service/               # 【AI处理服务】
│   │   ├── requirements.txt      # Python依赖
│   │   ├── Dockerfile
│   │   ├── .env.example
│   │   │
│   │   ├── app/
│   │   │   ├── main.py           # FastAPI入口
│   │   │   ├── config.py         # API密钥等配置
│   │   │   │
│   │   │   ├── api/              # API路由(内部接口)
│   │   │   │   └── internal.py
│   │   │   │
│   │   │   ├── models/           # 数据模型
│   │   │   │   ├── scene.py
│   │   │   │   ├── character.py
│   │   │   │   └── task.py
│   │   │   │
│   │   │   ├── services/         # 核心业务逻辑
│   │   │   │   ├── text_analyzer.py      # 文本分析(GPT-4/Claude)
│   │   │   │   ├── image_generator.py    # 图像生成(Midjourney)
│   │   │   │   ├── voice_generator.py    # 配音生成(阿里云TTS)
│   │   │   │   ├── character_manager.py  # 角色一致性管理
│   │   │   │   └── oss_client.py         # 对象存储客户端
│   │   │   │
│   │   │   ├── workers/          # Celery异步任务
│   │   │   │   ├── __init__.py
│   │   │   │   ├── celery_app.py # Celery配置
│   │   │   │   └── tasks.py      # 异步任务定义
│   │   │   │
│   │   │   └── utils/            # 工具函数
│   │   │       ├── prompt_builder.py  # Prompt工程
│   │   │       └── retry.py           # 重试机制
│   │   │
│   │   └── tests/
│   │       ├── test_text_analyzer.py
│   │       └── test_image_generator.py
│   │
│   └── video-service/            # 【视频合成服务】
│       ├── requirements.txt
│       ├── Dockerfile
│       ├── .env.example
│       │
│       ├── app/
│       │   ├── main.py           # FastAPI入口
│       │   ├── config.py
│       │   │
│       │   ├── api/
│       │   │   ├── internal.py   # 内部API(接收AI服务数据)
│       │   │   └── callbacks.py  # 回调接口
│       │   │
│       │   ├── models/
│       │   │   ├── scene.py
│       │   │   └── video_job.py
│       │   │
│       │   ├── services/
│       │   │   ├── video_composer.py     # 视频合成主逻辑
│       │   │   ├── ffmpeg_executor.py    # FFmpeg封装
│       │   │   ├── subtitle_renderer.py  # 字幕渲染
│       │   │   └── oss_client.py
│       │   │
│       │   ├── workers/          # Celery任务
│       │   │   ├── celery_app.py
│       │   │   └── tasks.py
│       │   │
│       │   └── utils/
│       │       ├── ffmpeg_builder.py  # FFmpeg命令构建器
│       │       └── media_utils.py     # 媒体处理工具
│       │
│       └── tests/
│           └── test_video_composer.py
│
├── shared/                       # 【共享代码】
│   ├── __init__.py
│   ├── constants.py              # 常量定义
│   ├── enums.py                  # 枚举类型
│   └── exceptions.py             # 自定义异常
│
├── docs/                         # 【文档目录】
│   ├── api/                      # API文档
│   │   ├── frontend-to-gateway.md
│   │   └── gateway-to-services.md
│   ├── deployment/               # 部署文档
│   │   ├── docker.md
│   │   └── production.md
│   └── development/              # 开发文档
│       ├── setup.md              # 环境搭建
│       └── workflow.md           # 开发流程
│
├── scripts/                      # 【工具脚本】
│   ├── setup.sh                  # 一键环境搭建
│   ├── start-dev.sh              # 启动开发环境
│   ├── build.sh                  # 构建脚本
│   └── deploy.sh                 # 部署脚本
│
└── docker/                       # 【Docker配置】
    ├── nginx/                    # Nginx配置
    │   └── nginx.conf
    ├── redis/                    # Redis配置
    │   └── redis.conf
    └── docker-compose.dev.yml    # 开发环境编排
```

---

## 目录说明

### 1. frontend/ - 前端模块

**负责人**: 前端工程师

**技术栈**: React/Vue + TypeScript + Vite/Webpack

**关键文件**:
- `src/services/taskService.ts` - 封装与API Gateway的交互
- `src/hooks/usePolling.ts` - 实现任务状态轮询
- `src/pages/TaskCreate/` - 任务创建页面(文本上传)

**开发命令**:
```bash
cd frontend
npm install
npm run dev          # 启动开发服务器
npm run build        # 构建生产版本
```

---

### 2. backend/api-gateway/ - API网关

**负责人**: 可由任意后端工程师负责(或前端工程师)

**职责**:
- 统一前端入口
- 路由转发到AI服务
- 任务状态查询(从Redis)

**关键文件**:
- `app/api/tasks.py` - 任务CRUD接口
- `app/services/task_service.py` - 任务业务逻辑

**启动命令**:
```bash
cd backend/api-gateway
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### 3. backend/ai-service/ - AI处理服务

**负责人**: AI工程师

**职责**:
- 文本分析(调用GPT-4/Claude)
- 图像生成(调用Midjourney API)
- 配音生成(调用阿里云TTS)
- 角色一致性管理

**关键文件**:
- `app/services/text_analyzer.py` - 场景分割与角色识别
- `app/services/image_generator.py` - Midjourney调用(含--cref逻辑)
- `app/services/character_manager.py` - 角色库管理
- `app/workers/tasks.py` - Celery异步任务

**环境变量** (`.env`):
```env
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
MIDJOURNEY_API_KEY=xxx
ALIYUN_TTS_ACCESS_KEY=xxx
ALIYUN_TTS_SECRET_KEY=xxx
OSS_ENDPOINT=xxx
OSS_BUCKET=xxx
REDIS_URL=redis://localhost:6379/0
```

**启动命令**:
```bash
# 启动API服务
uvicorn app.main:app --reload

# 启动Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

---

### 4. backend/video-service/ - 视频合成服务

**负责人**: 视频工程师

**职责**:
- 接收场景数据
- FFmpeg视频合成
- 字幕叠加
- 上传到OSS

**关键文件**:
- `app/services/video_composer.py` - 视频合成主流程
- `app/services/ffmpeg_executor.py` - FFmpeg命令封装
- `app/utils/ffmpeg_builder.py` - FFmpeg命令构建器

**环境变量**:
```env
OSS_ENDPOINT=xxx
OSS_BUCKET=xxx
REDIS_URL=redis://localhost:6379/0
```

**启动命令**:
```bash
# 启动API服务
uvicorn app.main:app --port 8002 --reload

# 启动Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

---

### 5. shared/ - 共享代码

**作用**: 避免重复代码,统一常量和类型定义

**示例** (`shared/constants.py`):
```python
# 任务状态
TASK_STATUS_PENDING = "pending"
TASK_STATUS_PROCESSING = "processing"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"

# OSS路径
OSS_PATH_CHARACTERS = "characters/"
OSS_PATH_SCENES = "scenes/"
OSS_PATH_AUDIO = "audio/"
OSS_PATH_VIDEOS = "videos/"
```

---

### 6. docs/ - 文档

**作用**: 集中管理所有文档,便于团队协作

---

### 7. scripts/ - 工具脚本

**示例** (`scripts/start-dev.sh`):
```bash
#!/bin/bash
# 一键启动所有开发环境

# 启动Redis
docker-compose up -d redis

# 启动后端服务
cd backend/api-gateway && uvicorn app.main:app --port 8000 &
cd backend/ai-service && uvicorn app.main:app --port 8001 &
cd backend/video-service && uvicorn app.main:app --port 8002 &

# 启动前端
cd frontend && npm run dev &

echo "所有服务已启动!"
```

---

## 3人协作工作流

### Day 1 上午:环境搭建

**前端工程师**:
```bash
git clone <仓库地址>
cd tfboys/frontend
npm install
npm run dev  # 启动开发服务器,可先用Mock数据
```

**AI工程师**:
```bash
cd tfboys/backend/ai-service
pip install -r requirements.txt
# 配置.env文件(API密钥)
uvicorn app.main:app --port 8001 --reload
```

**视频工程师**:
```bash
cd tfboys/backend/video-service
pip install -r requirements.txt
# 安装FFmpeg
sudo apt-get install ffmpeg  # Linux
# brew install ffmpeg         # macOS
uvicorn app.main:app --port 8002 --reload
```

---

### Day 1 下午 - Day 2:并行开发

#### 前端工程师工作内容
1. 实现 `src/services/taskService.ts`:
   ```typescript
   export const createTask = (novelText: string) => {
     return axios.post('/api/tasks', { novel_text: novelText })
   }
   
   export const getTaskStatus = (taskId: string) => {
     return axios.get(`/api/tasks/${taskId}`)
   }
   ```

2. 实现 `src/pages/TaskCreate/index.tsx` - 文本上传页
3. 实现 `src/pages/TaskList/index.tsx` - 任务列表页(轮询状态)

#### AI工程师工作内容
1. 实现 `text_analyzer.py` - 调用GPT-4分析文本
2. 实现 `image_generator.py` - 调用Midjourney生成图像
3. 实现 `character_manager.py` - 角色一致性管理
4. 实现 `voice_generator.py` - 调用阿里云TTS

#### 视频工程师工作内容
1. 实现 `ffmpeg_builder.py` - FFmpeg命令构建
2. 实现 `video_composer.py` - 视频合成主逻辑
3. 实现 `subtitle_renderer.py` - 字幕叠加

---

## 接口联调

### 前端 ↔ API Gateway
- 接口定义见 `API.md`
- 前端调用: `POST /api/tasks`
- 轮询状态: `GET /api/tasks/{task_id}`

### AI服务 ↔ 视频服务
- AI服务调用: `POST http://video-service:8002/internal/video-synthesis/jobs`
- 视频服务回调: `POST http://ai-service:8001/callbacks/video-completed`

---

## 部署说明

### Docker Compose启动(推荐开发环境)

```bash
docker-compose up -d
```

**docker-compose.yml** 示例:
```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  api-gateway:
    build: ./backend/api-gateway
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
  
  ai-service:
    build: ./backend/ai-service
    ports:
      - "8001:8001"
    env_file:
      - ./backend/ai-service/.env
  
  video-service:
    build: ./backend/video-service
    ports:
      - "8002:8002"
    env_file:
      - ./backend/video-service/.env
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
```

---

## 开发注意事项

### 1. 环境变量管理
- 各服务的 `.env` 文件 **不要提交到Git**
- 提供 `.env.example` 作为模板

### 2. 代码风格
- 前端: ESLint + Prettier
- 后端: Black + isort (Python)

### 3. Git工作流
- 功能分支: `feature/前端-任务列表页`
- Bug修复: `fix/视频合成-音频同步问题`

### 4. 测试
- 前端: Jest + React Testing Library
- 后端: Pytest

---

## 快速开始

```bash
# 1. 克隆仓库
git clone <仓库地址>
cd tfboys

# 2. 启动依赖服务(Redis)
docker-compose up -d redis

# 3. 启动后端服务
./scripts/start-backend.sh

# 4. 启动前端
cd frontend && npm install && npm run dev

# 访问 http://localhost:3000
```

---

**总结**: 本目录结构遵循**关注点分离**原则,前后端独立开发,通过API接口协作,适合3人团队并行开发,可在2天内完成MVP。
