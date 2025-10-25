# 七牛 AI Token API 功能测试指南

本指南将帮助您逐步测试迁移到七牛 AI Token API 后的功能。

## 📋 测试前准备

### 1. 获取七牛 API Key

访问 [七牛开发者中心](https://portal.qiniu.com/kodo/ak-sk) 获取您的 API Key。

### 2. 配置环境变量

编辑 `.env` 文件：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service
cp .env.example .env
```

在 `.env` 文件中设置：

```env
# 必需: 七牛 AI Token API Key
QINIU_API_KEY=your-qiniu-ai-token-api-key

# 可选: 七牛 TTS 服务
QINIU_ACCESS_KEY=your-qiniu-access-key
QINIU_SECRET_KEY=your-qiniu-secret-key

# 基础配置
REDIS_URL=redis://localhost:6379/0
VIDEO_SERVICE_URL=http://localhost:8002
```

### 3. 启动 Redis

```bash
# 方式 1: 使用 Docker
docker run -d -p 6379:6379 redis:latest

# 方式 2: 使用 Docker Compose
docker-compose up -d redis

# 方式 3: 本地 Redis (如已安装)
redis-server
```

### 4. 安装依赖（如未安装）

```bash
# 在项目根目录
cd /Users/jiangzhi/repo/tfboys
pip install -e ./shared

# 在 ai-service 目录
cd backend/ai-service
pip install -r requirements.txt
```

---

## 🧪 测试步骤

### 步骤 1: 快速验证 - 单元测试

先运行单元测试，确保代码逻辑正确：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service

# 测试文本分析器（已迁移到七牛）
python3 -m pytest tests/unit/services/test_text_analyzer.py -v

# 测试图像生成器（已迁移到七牛）
python3 -m pytest tests/unit/services/test_image_generator.py -v
```

**预期结果:**
- 文本分析器: 7/7 测试通过 ✅
- 图像生成器: 部分通过（storage mock 问题）

---

### 步骤 2: 功能测试 - 文本分析

使用集成测试脚本测试实际的七牛 API 调用：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service

# 仅测试文本分析
python3 test_qiniu_integration.py --test text
```

**测试内容:**
- ✅ 调用七牛 AI 推理 API (DeepSeek-V3)
- ✅ 分析小说文本
- ✅ 生成场景列表
- ✅ 识别角色
- ✅ 归一化角色描述

**预期输出:**
```
🧪 测试文本分析 (七牛 AI 推理 API - DeepSeek-V3)
============================================================
📝 输入文本长度: 234 字符
正在调用七牛 AI 推理 API...

✅ 分析成功！生成了 2 个场景

场景 1:
  描述: 清晨的校园,樱花盛开...
  旁白: 春天的早晨,校园里樱花盛开...
  角色数: 1
    - 小明: 少年,黑色短发,蓝色眼睛...
```

---

### 步骤 3: 功能测试 - 图像生成

测试七牛文生图 API：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service

# 仅测试图像生成
python3 test_qiniu_integration.py --test image
```

**测试内容:**
- ✅ 生成角色设定图
- ✅ 生成场景图像
- ✅ 测试不同宽高比 (1:1, 16:9, 9:16)
- ✅ 保存图像到本地

**预期输出:**
```
🎨 测试图像生成 (七牛文生图 API - Gemini 2.5 Flash)
============================================================
📸 测试 1: 生成角色设定图
角色: 小明 (黑色短发，蓝色眼睛的少年)
✅ 图像已生成: /tmp/tfboys/characters/小明.png
   文件大小: 245.67 KB

📸 测试 2: 生成场景图像
场景: 春天的校园，樱花飘落
✅ 场景图像已生成: /tmp/tfboys/scenes/test_scene_001.png
   文件大小: 312.45 KB

📁 生成的图像保存在: /tmp/tfboys/
```

**验证生成的图像:**
```bash
# 查看生成的图像
ls -lh /tmp/tfboys/characters/
ls -lh /tmp/tfboys/scenes/

# 在 Mac 上预览图像
open /tmp/tfboys/characters/小明.png
open /tmp/tfboys/scenes/test_scene_001.png
```

---

### 步骤 4: 完整功能测试

同时测试所有功能：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service

# 测试所有功能
python3 test_qiniu_integration.py --test all
```

---

### 步骤 5: 启动服务进行端到端测试

启动 AI Service 并通过 API 端点测试：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**访问 API 文档:**
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

**测试 API 端点:**

```bash
# 1. 健康检查
curl http://localhost:8001/health

# 2. 提交文本分析任务（需要 Redis）
curl -X POST http://localhost:8001/internal/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_001",
    "novel_text": "春天的早晨，校园里樱花盛开。小明走在林荫道上。"
  }'

# 3. 查询任务状态
curl http://localhost:8001/internal/tasks/test_001
```

---

## 🐛 故障排除

### 问题 1: ImportError: No module named 'shared'

**解决方案:**
```bash
cd /Users/jiangzhi/repo/tfboys
pip install -e ./shared
```

### 问题 2: QINIU_API_KEY is required

**解决方案:**
检查 `.env` 文件是否正确配置：
```bash
cat backend/ai-service/.env | grep QINIU_API_KEY
```

### 问题 3: Connection refused to Redis

**解决方案:**
```bash
# 确保 Redis 正在运行
docker ps | grep redis

# 或启动 Redis
docker run -d -p 6379:6379 redis:latest
```

### 问题 4: API 调用失败

**检查清单:**
- ✅ API Key 是否正确
- ✅ 网络连接是否正常
- ✅ 七牛 API 服务是否可用

**查看详细日志:**
```bash
# 启动服务时查看日志
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

---

## 📊 测试检查清单

### 文本分析功能
- [ ] 单元测试通过
- [ ] 功能测试成功调用七牛 API
- [ ] 成功生成场景列表
- [ ] 角色识别正确
- [ ] 场景描述合理

### 图像生成功能
- [ ] 单元测试部分通过
- [ ] 功能测试成功生成角色图
- [ ] 功能测试成功生成场景图
- [ ] 不同宽高比都能生成
- [ ] 图像文件正常保存

### 服务集成
- [ ] 服务可以正常启动
- [ ] API 文档可访问
- [ ] 健康检查端点正常
- [ ] 可以通过 API 调用功能

---

## 📈 性能测试（可选）

### 测试响应时间

```bash
# 测试文本分析性能
time python3 test_qiniu_integration.py --test text

# 测试图像生成性能
time python3 test_qiniu_integration.py --test image
```

### 并发测试

使用 Apache Bench 或类似工具测试并发请求：

```bash
# 安装 ab (如未安装)
# Mac: brew install httpd
# Ubuntu: apt-get install apache2-utils

# 测试健康检查端点
ab -n 100 -c 10 http://localhost:8001/health
```

---

## ✅ 测试完成标准

当以下所有项都完成时，表示迁移测试成功：

1. ✅ 单元测试: 文本分析 7/7 通过
2. ✅ 功能测试: 文本分析成功
3. ✅ 功能测试: 图像生成成功
4. ✅ 服务启动: 无错误
5. ✅ API 调用: 正常响应
6. ✅ 生成结果: 质量符合预期

---

## 📝 反馈与报告

测试完成后，请记录：

1. **成功的测试**: 哪些功能正常工作
2. **失败的测试**: 错误信息和堆栈跟踪
3. **性能数据**: 响应时间、成功率
4. **生成质量**: 文本分析准确性、图像质量

**示例测试报告:**
```
测试时间: 2024-10-25
测试环境: macOS, Python 3.9

✅ 文本分析: 成功
   - 响应时间: 3.2s
   - 场景数: 2
   - 准确性: 高

✅ 图像生成: 成功
   - 响应时间: 8.5s
   - 图像质量: 良好
   - 文件大小: 250KB 平均

⚠️  发现的问题:
   - 无
```

---

## 🚀 下一步

测试通过后，您可以：

1. **集成到完整工作流**: 测试端到端的视频生成
2. **性能优化**: 调整参数提升速度和质量
3. **部署到生产**: 使用 Docker Compose 部署
4. **监控和日志**: 设置监控和告警

祝测试顺利！🎉
