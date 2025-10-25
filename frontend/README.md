# TFBoys AI - Frontend

TFBoys AI 前端项目 - 小说文本一键生成动漫视频的 Web 应用

---

## 🛠️ 技术栈

### 核心框架
- **React 18.3+** - 用户界面构建框架
- **TypeScript 5.6+** - 类型安全的 JavaScript 超集
- **Vite 6.0+** - 下一代前端构建工具

### UI 组件库
- **Tailwind CSS 3.4+** - 原子化 CSS 框架
- **Radix UI** - 无样式的可访问性组件库
- **Lucide React** - 精美的 React 图标库
- **shadcn/ui** - 基于 Radix UI 的可定制组件库

### 状态管理与数据请求
- **SWR 2.2+** - React Hooks 数据请求库

### 样式方案
- **Emotion** - CSS-in-JS 库
- **PostCSS** - CSS 转换工具
- **Autoprefixer** - CSS 自动添加浏览器前缀

### 开发工具
- **ESLint** - 代码质量检查工具
- **TypeScript ESLint** - TypeScript 代码检查插件

---

## 📁 目录结构

```
frontend/
├── docs/                      # 文档目录
│   ├── PRODUCT_DESIGN.md      # 产品设计文档
│   └── mockups/               # 原型图目录
│       ├── video-generation-page.svg    # 视频生成页面原型
│       ├── my-tasks-page.svg           # 我的任务页面原型
│       ├── video-preview-dialog.svg    # 视频预览弹窗原型
│       └── README.md                   # 原型图说明
│
├── public/                    # 静态资源目录
│   └── vite.svg              # Vite Logo
│
├── src/                      # 源代码目录
│   ├── components/           # React 组件
│   │   └── ui/              # UI 基础组件 (shadcn/ui)
│   │       ├── button.tsx   # 按钮组件
│   │       └── card.tsx     # 卡片组件
│   ├── App.tsx              # 根组件
│   ├── main.tsx             # 应用入口
│   ├── index.css            # 全局样式
│   └── vite-env.d.ts        # Vite 环境类型定义
│
├── index.html                # HTML 入口文件
├── package.json              # 项目依赖配置
├── tsconfig.json             # TypeScript 配置
├── tsconfig.app.json         # 应用 TypeScript 配置
├── tsconfig.node.json        # Node.js TypeScript 配置
├── vite.config.ts            # Vite 配置
├── tailwind.config.js        # Tailwind CSS 配置
├── postcss.config.js         # PostCSS 配置
├── eslint.config.js          # ESLint 配置
├── components.json           # shadcn/ui 组件配置
└── README.md                 # 项目说明文档
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
