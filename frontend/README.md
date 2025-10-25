# TFBoys AI - Frontend

TFBoys AI 前端项目 - 小说文本一键生成动漫视频的 Web 应用

---

## 🛠️ 技术栈

### 核心框架
- **Vite 6.x** - 下一代前端构建工具，提供极速的开发体验
- **React 18.3** - 现代化 UI 框架，支持并发特性
- **TypeScript 5.6** - 类型安全的 JavaScript 超集

### UI 组件与样式
- **Tailwind CSS 3.4** - 实用优先的 CSS 框架
- **shadcn/ui** - 基于 Radix UI 的高质量组件库
- **framer-motion 11.x** - 生产级 React 动画库
- **lucide-react** - 优雅的图标库

### 状态管理与数据获取
- **SWR 2.x** - React Hooks 数据获取库，支持缓存和自动重验证

### 开发工具
- **ESLint 9.x** - 代码质量检查
- **PostCSS** - CSS 处理工具
- **pnpm** - 快速、节省磁盘空间的包管理器

---

## 📁 目录结构

```
frontend/
├── public/              # 静态资源文件
├── src/
│   ├── components/      # React 组件
│   │   └── ui/          # shadcn/ui 基础组件
│   │       ├── button.tsx
│   │       └── card.tsx
│   ├── App.tsx          # 根组件
│   ├── main.tsx         # 应用入口
│   ├── index.css        # 全局样式
│   └── vite-env.d.ts    # Vite 类型定义
├── docs/                # 项目文档
│   ├── PRODUCT_DESIGN.md  # 产品设计文档
│   └── mockups/         # 原型图
├── components.json      # shadcn/ui 配置
├── tailwind.config.js   # Tailwind CSS 配置
├── vite.config.ts       # Vite 配置
├── tsconfig.json        # TypeScript 配置
└── package.json         # 项目依赖

```

---

## 📚 文档导航

### 核心文档

📖 **[产品设计文档](./docs/PRODUCT_DESIGN.md)** - **必读**
- 产品经理产出：产品概述、User Story、业务流程图
- 设计师产出：线框图、原型图、设计系统

### 原型图

🎨 **[原型图目录](./docs/mockups/)**
- `video-generation-page.svg` - 视频生成页面
- `my-tasks-page.svg` - 我的任务页面
- `video-preview-dialog.svg` - 视频预览弹窗
- `README.md` - 原型图说明

---

## 🎯 产品核心

### 产品定位
小说文本自动生成动漫视频的 Web 应用

### 核心价值
- 🤖 **自动化创作** - 将文字转化为视觉内容
- 🎭 **角色一致性** - AI 保证角色视觉一致性
- ⚡ **快速生成** - 全自动流程，用户只需等待
- 🎨 **风格可定制** - 支持多种视频风格

### 目标用户
- 📚 小说作者 - 为作品制作宣传视频
- 🎬 内容创作者 - 快速生成视频内容
- 🌟 二次元爱好者 - 小说片段可视化
