# API Gateway - TFBoys API网关服务

统一的API入口,负责路由请求到不同的后端服务。

## 主要功能

- 🔀 请求路由和转发
- 📊 任务状态查询(从Redis)
- 🔒 CORS配置
- 📝 API文档(Swagger)

## 技术栈

- FastAPI
- Redis (任务状态存储)
- HTTPX (异步HTTP客户端)

## 目录结构

```
app/
├── api/                # API路由
│   ├── tasks.py       # 任务相关路由
│   └── health.py      # 健康检查
├── models/             # 数据模型
│   └── task.py
├── services/           # 业务逻辑
│   └── redis_client.py
├── config.py           # 配置管理
└── main.py             # FastAPI应用入口
```

## API端点

### 任务管理

- `POST /api/tasks` - 创建任务
- `GET /api/tasks/{task_id}` - 获取任务详情
- `GET /api/tasks` - 获取任务列表
- `DELETE /api/tasks/{task_id}` - 删除任务

### 健康检查

- `GET /health` - 健康检查

## 开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件
```

### 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

访问 API文档: http://localhost:8000/docs

## Docker部署

```bash
docker build -t tfboys-api-gateway .
docker run -p 8000:8000 --env-file .env tfboys-api-gateway
```

## 与其他服务的交互

### AI Service
- 转发任务创建请求到AI服务
- URL: `http://ai-service:8001`

### Redis
- 存储和查询任务状态
- 存储任务列表
