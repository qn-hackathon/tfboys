# TFBoys - 文字内容的短视频传播加速平台

Token Free Boys - 文字内容的短视频传播加速平台

## 项目简介

本项目实现了一个自动化的文字生成视频系统,可以将小说文字自动转换为动漫风格的视频。视频由图片、文字和配音三部分组成,并保证角色的视觉一致性。

### 核心特性

- 🎨 **角色一致性**: 通过详细的提示词描述保证角色在不同场景的视觉一致性
- 🤖 **AI驱动**: 基于七牛 AI Token API，使用 DeepSeek-V3 进行文本分析，Gemini 2.5 Flash 生成图像，七牛 TTS 生成配音
- 🎬 **自动化视频合成**: 使用FFmpeg自动合成图片、字幕和音频
- 📦 **Monorepo架构**: 前后端代码在同一仓库,便于管理和部署
- 🐳 **Docker支持**: 完整的Docker配置,一键启动所有服务

## 技术栈

### 前端

[前端技术栈](https://github.com/qn-hackathon/tfboys/blob/main/frontend/README.md#%EF%B8%8F-%E6%8A%80%E6%9C%AF%E6%A0%88)


### 后端
- Python + FastAPI
- Celery + Redis (异步任务队列)
- 七牛 AI Token API
  - DeepSeek-V3 (文本分析)
  - Gemini 2.5 Flash (图像生成)
  - 七牛 TTS (配音生成)
- FFmpeg (视频合成)

## 快速开始

### 方式一: Docker Compose (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/qn-hackathon/tfboys.git
cd tfboys

# 2. 配置环境变量
cp backend/ai-service/.env.example backend/ai-service/.env
cp backend/video-service/.env.example backend/video-service/.env
# 编辑.env文件,填入API密钥

# 3. 启动所有服务
make up

# 4. 访问应用
open http://localhost:3000
```

### 方式二: 本地开发

```bash
# 1. 安装依赖
make install

# 2. 启动Redis
docker-compose up -d redis

# 3. 启动后端服务(需要3个终端)
cd backend/api-gateway && uvicorn app.main:app --reload --port 8000
cd backend/ai-service
export PYTHONPATH="$(cd ../.. && pwd)"
uvicorn app.main:app --reload --port 8001
cd backend/video-service && uvicorn app.main:app --reload --port 8002

# 4. 启动前端
cd frontend && npm run dev
```

## 项目结构

```
tfboys/
├── frontend/              # 前端应用(React)
├── backend/               # 后端服务
│   ├── api-gateway/      # API网关
│   ├── ai-service/       # AI处理服务
│   └── video-service/    # 视频合成服务
├── shared/                # 共享代码
├── docs/                  # 文档
├── scripts/               # 工具脚本
└── docker/                # Docker配置
```

详细的目录结构说明请查看 [CLAUDE.md](./CLAUDE.md)

## 文档

- [安装与启动指南](./安装与启动指南.md) - 环境配置、安装步骤、启动方式、常见问题
- [架构设计文档](./架构设计文档.md) - 系统架构、技术栈、数据模型、业务流程
- [团队分工文档](./团队分工文档.md) - 模块职责、人员分工、协作方式
- [AI开发指南](./CLAUDE.md) - 项目结构、开发规范、业务逻辑
- [前端产品设计](./frontend/docs/PRODUCT_DESIGN.md) - 前端页面设计和交互流程

## 开发指南

### 3人协作模式

本项目设计为3人并行开发:

| 角色 | 负责模块 | 工作目录 |
|------|----------|----------|
| 前端工程师 | Web UI | `frontend/` |
| AI工程师 | 文本分析、图像生成、配音 | `backend/ai-service/` |
| 视频工程师 | 视频合成 | `backend/video-service/` |

### 常用命令

```bash
make help      # 查看所有可用命令
make install   # 安装依赖
make dev       # 启动开发环境
make build     # 构建Docker镜像
make test      # 运行测试
make clean     # 清理临时文件
```

## API文档

- API Gateway: http://localhost:8000/docs
- AI Service: http://localhost:8001/docs
- Video Service: http://localhost:8002/docs

## 环境变量

各服务需要配置以下环境变量:

### AI Service (.env)
```env
# 七牛 AI Token API 配置
QINIU_API_KEY=your-qiniu-ai-token-api-key

# 七牛 TTS 服务配置
QINIU_ACCESS_KEY=your-qiniu-access-key
QINIU_SECRET_KEY=your-qiniu-secret-key

# Redis 配置
REDIS_URL=redis://localhost:6379/0
```

### Video Service (.env)
```env
# Redis 配置
REDIS_URL=redis://localhost:6379/0
```

## License

MIT

## 贡献

欢迎提交Issue和Pull Request!
