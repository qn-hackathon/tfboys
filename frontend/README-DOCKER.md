# 前端 Docker 部署文档

## 📦 技术栈

- **前端框架**: React 18 + TypeScript
- **构建工具**: Vite 6
- **包管理器**: pnpm
- **Web 服务器**: Nginx 1.25
- **Docker**: 多阶段构建

## 🚀 快速开始

### 方式一: 使用 docker-compose (推荐)

在项目根目录运行:

```bash
# 构建并启动所有服务(包括前端)
docker compose up -d

# 仅构建前端
docker compose build frontend

# 仅启动前端
docker compose up -d frontend

# 查看前端日志
docker compose logs -f frontend
```

### 方式二: 独立构建和运行

在 `frontend/` 目录运行:

```bash
# 一键构建并运行
./build-docker.sh

# 或手动执行
docker build -t tfboys-frontend:latest .
docker run -d --name tfboys-frontend -p 3000:80 tfboys-frontend:latest
```

## 📝 构建说明

### Dockerfile 多阶段构建

```dockerfile
# 阶段 1: 构建阶段 (node:20-alpine)
- 安装 pnpm
- 安装依赖 (pnpm install --frozen-lockfile)
- 构建生产版本 (pnpm run build)
- 输出目录: dist/

# 阶段 2: 生产阶段 (nginx:1.25-alpine)
- 复制 nginx 配置
- 复制构建产物到 /usr/share/nginx/html
- 暴露端口 80
- 启动 Nginx
```

### 构建命令

```bash
# 本地构建(开发)
pnpm install
pnpm run build

# Docker 构建
docker build -t tfboys-frontend:latest .
```

## 🌐 访问地址

- **前端应用**: http://localhost:3000
- **健康检查**: http://localhost:3000/health
- **API 代理**: http://localhost:3000/api/ → http://api-gateway:8001/

## 📂 目录结构

```
frontend/
├── Dockerfile              # Docker 构建文件
├── nginx.conf              # Nginx 配置
├── .dockerignore           # Docker 忽略文件
├── build-docker.sh         # 一键构建脚本
├── package.json            # 项目依赖
├── vite.config.ts          # Vite 配置
├── src/                    # 源代码
│   ├── components/         # React 组件
│   ├── pages/              # 页面
│   └── ...
└── dist/                   # 构建输出(不提交到 Git)
```

## 🔧 配置说明

### Nginx 配置 (nginx.conf)

- **Gzip 压缩**: 启用,优化传输
- **静态资源缓存**: 1 年,提高性能
- **SPA 路由支持**: 所有路由返回 index.html
- **API 代理**: /api/ → http://api-gateway:8001/
- **健康检查**: /health 端点

### Docker 配置

- **基础镜像**: node:20-alpine (构建), nginx:1.25-alpine (运行)
- **端口映射**: 3000:80
- **健康检查**: 每 30 秒检查一次
- **重启策略**: unless-stopped

## 🧪 测试部署

### 1. 构建镜像

```bash
cd frontend
docker build -t tfboys-frontend:latest .
```

### 2. 运行容器

```bash
docker run -d \
  --name tfboys-frontend \
  -p 3000:80 \
  tfboys-frontend:latest
```

### 3. 验证部署

```bash
# 检查容器状态
docker ps | grep tfboys-frontend

# 测试健康检查
curl http://localhost:3000/health

# 测试首页
curl http://localhost:3000/

# 在浏览器访问
open http://localhost:3000
```

### 4. 查看日志

```bash
# 实时日志
docker logs -f tfboys-frontend

# 最近 100 行
docker logs --tail 100 tfboys-frontend
```

## 🐛 常见问题

### 1. 端口 3000 被占用

**解决方案**: 修改 docker-compose.yml 或 docker run 命令中的端口映射

```bash
# 使用 8080 端口
docker run -d --name tfboys-frontend -p 8080:80 tfboys-frontend:latest
```

### 2. 构建失败: pnpm install 超时

**解决方案**: 使用国内镜像源

```bash
# 在 Dockerfile 中添加
RUN pnpm config set registry https://registry.npmmirror.com
```

### 3. 访问 /api/ 返回 502

**原因**: Nginx 无法连接到 api-gateway 服务

**解决方案**:
- 确保 api-gateway 服务已启动
- 使用 docker-compose 启动(自动配置网络)
- 检查 nginx.conf 中的 proxy_pass 配置

### 4. 页面刷新 404

**原因**: Nginx 未正确配置 SPA 路由

**解决方案**: 已在 nginx.conf 中配置 `try_files $uri $uri/ /index.html;`

## 📊 性能优化

### 1. 构建优化

- ✅ 使用 pnpm (比 npm 快 2-3 倍)
- ✅ 使用 --frozen-lockfile (锁定依赖版本)
- ✅ 多阶段构建 (最终镜像仅 ~25MB)
- ✅ .dockerignore (减少构建上下文)

### 2. 运行时优化

- ✅ Gzip 压缩 (减少 70% 传输大小)
- ✅ 静态资源缓存 (1 年)
- ✅ Nginx 性能配置

### 3. 镜像大小

```
构建阶段镜像: ~500MB (node:20-alpine + 依赖)
最终运行镜像: ~25MB (nginx:1.25-alpine + 构建产物)
```

## 🔄 CI/CD 集成

### GitHub Actions 示例

```yaml
name: Build and Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker Image
        run: |
          cd frontend
          docker build -t tfboys-frontend:${{ github.sha }} .
      
      - name: Push to Registry
        run: |
          docker tag tfboys-frontend:${{ github.sha }} registry.example.com/tfboys-frontend:latest
          docker push registry.example.com/tfboys-frontend:latest
```

## 📚 相关文档

- [项目总文档](../CLAUDE.md)
- [Docker 部署指南](../DOCKER_DEPLOYMENT_GUIDE.md)
- [快速启动指南](../QUICK_START.md)
- [Vite 文档](https://vitejs.dev/)
- [Nginx 文档](https://nginx.org/en/docs/)

## 🤝 贡献

如需改进前端部署配置,请:
1. 修改 Dockerfile 或 nginx.conf
2. 测试构建和运行
3. 更新此文档
4. 提交 PR

---

**最后更新**: 2024-10-26
**维护者**: TFBoys Team
