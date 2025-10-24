# Frontend - TFBoys 前端应用

基于 React + TypeScript + Vite 的现代化前端应用。

## 主要功能

- 📝 小说文字上传
- 📊 任务状态监控(实时轮询)
- 🎬 视频预览和下载
- 📱 响应式设计

## 技术栈

- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design 5
- **路由**: React Router v6
- **HTTP客户端**: Axios
- **状态管理**: Zustand (预留)

## 目录结构

```
src/
├── pages/              # 页面组件
│   ├── Home/          # 首页
│   ├── TaskCreate/    # 任务创建页
│   ├── TaskList/      # 任务列表页
│   └── VideoPreview/  # 视频预览页
├── components/        # 公共组件
│   ├── Header/        # 顶部导航
│   └── Footer/        # 底部
├── services/          # API服务层
│   ├── api.ts        # Axios配置
│   └── taskService.ts # 任务相关API
├── hooks/             # 自定义Hooks
│   └── usePolling.ts  # 轮询Hook
├── types/             # TypeScript类型
└── utils/             # 工具函数
```

## 开发

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 运行测试

```bash
npm test
```

## API集成

前端通过代理访问后端API:

- 开发环境: Vite代理 `/api` → `http://localhost:8000`
- 生产环境: Nginx反向代理

## 主要页面

### 1. 首页 (Home)
- 功能介绍
- 快捷入口

### 2. 创建任务 (TaskCreate)
- 文本输入框
- 提交创建任务

### 3. 任务列表 (TaskList)
- 显示所有任务
- 自动轮询更新状态
- 支持筛选和分页

### 4. 视频预览 (VideoPreview)
- 实时显示生成进度
- 视频播放器
- 下载视频

## 环境变量

开发环境已在 vite.config.ts 中配置代理，无需额外环境变量。

## Docker部署

```bash
docker build -t tfboys-frontend .
docker run -p 3000:80 tfboys-frontend
```

## 贡献指南

1. 遵循 TypeScript 严格模式
2. 使用 ESLint 进行代码检查
3. 组件使用函数式写法 + Hooks
4. 页面组件放在 pages/ 目录
5. 可复用组件放在 components/ 目录
