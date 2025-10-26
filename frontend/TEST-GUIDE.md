# 前端 Docker 部署测试指南

## 🧪 测试步骤

### 1. 本地测试 Docker 构建

在 `frontend/` 目录下运行:

```bash
# 方式一: 使用一键脚本
./build-docker.sh

# 方式二: 手动构建
docker build -t tfboys-frontend:latest .
```

**预期结果**:
- ✅ 构建成功
- ✅ 镜像大小约 25MB
- ✅ 无构建错误

### 2. 运行容器测试

```bash
# 启动容器
docker run -d \
  --name tfboys-frontend-test \
  -p 3000:80 \
  tfboys-frontend:latest

# 等待启动
sleep 5
```

### 3. 健康检查测试

```bash
# 测试健康检查端点
curl http://localhost:3000/health

# 预期输出: healthy
```

### 4. 首页访问测试

```bash
# 测试首页
curl -I http://localhost:3000/

# 预期: HTTP/1.1 200 OK
```

### 5. 静态资源测试

```bash
# 测试 JS 文件
curl -I http://localhost:3000/assets/index-*.js

# 预期: 
# - HTTP/1.1 200 OK
# - Cache-Control: public, immutable
# - Content-Encoding: gzip
```

### 6. SPA 路由测试

```bash
# 测试前端路由(应返回 index.html)
curl -I http://localhost:3000/some-random-path

# 预期: HTTP/1.1 200 OK (返回 index.html)
```

### 7. API 代理测试

```bash
# 如果 api-gateway 正在运行
curl http://localhost:3000/api/health

# 预期: 代理到 api-gateway:8001/health
```

### 8. 浏览器测试

```bash
# 在浏览器打开
open http://localhost:3000

# 或手动访问 http://localhost:3000
```

**检查项**:
- ✅ 页面正常加载
- ✅ 样式正确显示
- ✅ 交互功能正常
- ✅ 无控制台错误

### 9. 容器日志检查

```bash
# 查看 Nginx 访问日志
docker logs tfboys-frontend-test

# 预期: 无错误日志
```

### 10. 清理测试环境

```bash
# 停止并删除容器
docker stop tfboys-frontend-test
docker rm tfboys-frontend-test

# 删除测试镜像(可选)
docker rmi tfboys-frontend:latest
```

## 🚀 使用 docker-compose 测试

### 1. 构建所有服务

```bash
# 在项目根目录
docker compose build
```

### 2. 启动前端服务

```bash
# 仅启动前端(及其依赖)
docker compose up -d frontend
```

### 3. 查看状态

```bash
# 检查容器状态
docker compose ps

# 预期: frontend 状态为 healthy
```

### 4. 测试访问

```bash
# 健康检查
curl http://localhost:3000/health

# 首页
curl http://localhost:3000/
```

### 5. 查看日志

```bash
# 实时日志
docker compose logs -f frontend
```

### 6. 停止服务

```bash
# 停止前端
docker compose stop frontend

# 停止所有服务
docker compose down
```

## ✅ 测试检查清单

### 构建阶段
- [ ] Docker 镜像构建成功
- [ ] 构建时间合理(首次 < 5分钟, 缓存后 < 1分钟)
- [ ] 镜像大小合理(< 50MB)
- [ ] 无构建警告或错误

### 运行阶段
- [ ] 容器成功启动
- [ ] 健康检查通过
- [ ] 端口 3000 可访问
- [ ] 首页正常显示

### 功能测试
- [ ] 静态资源正确加载(JS, CSS, 图片)
- [ ] Gzip 压缩生效
- [ ] 缓存头正确设置
- [ ] SPA 路由正常工作
- [ ] API 代理正常(如已配置)

### 性能测试
- [ ] 首次加载时间 < 2秒
- [ ] 资源加载并发正常
- [ ] 无内存泄漏
- [ ] CPU 使用率正常

## 🐛 故障排查

### 问题 1: 构建失败

```bash
# 检查 Docker 版本
docker --version

# 检查磁盘空间
df -h

# 清理 Docker 缓存
docker builder prune
```

### 问题 2: 容器无法启动

```bash
# 查看详细日志
docker logs --tail 100 tfboys-frontend

# 检查端口占用
lsof -i :3000

# 检查容器状态
docker inspect tfboys-frontend
```

### 问题 3: 页面 404

```bash
# 进入容器检查文件
docker exec -it tfboys-frontend sh
ls -la /usr/share/nginx/html/

# 检查 Nginx 配置
docker exec -it tfboys-frontend cat /etc/nginx/conf.d/default.conf
```

### 问题 4: API 代理 502

```bash
# 检查网络连接
docker network inspect tfboys-network

# 测试容器间连接
docker exec tfboys-frontend ping api-gateway

# 检查 api-gateway 是否运行
docker ps | grep api-gateway
```

## 📊 性能基准

### 构建性能
- 首次构建: 3-5 分钟
- 缓存构建: 30-60 秒
- 镜像大小: 20-30 MB

### 运行性能
- 启动时间: < 3 秒
- 内存占用: < 50 MB
- CPU 占用: < 5%

### 网络性能
- 首页加载: < 1 秒
- 静态资源: < 100ms
- API 代理延迟: < 50ms

## 🎯 验收标准

### 必须通过
1. ✅ Docker 镜像构建成功,无错误
2. ✅ 容器启动成功,健康检查通过
3. ✅ 外部可访问 http://localhost:3000
4. ✅ 首页正常显示,无控制台错误
5. ✅ 静态资源正确加载(JS, CSS, 图片)

### 建议通过
1. ✅ Gzip 压缩生效
2. ✅ 缓存头正确设置
3. ✅ SPA 路由正常工作
4. ✅ 镜像大小 < 50MB
5. ✅ 构建时间 < 5分钟(首次)

---

**测试通过标准**: 所有"必须通过"项 + 至少 3 个"建议通过"项

**最后更新**: 2024-10-26
