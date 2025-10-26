# AI 服务真实流程测试指南

本指南将帮助您逐步测试 AI 服务的完整工作流程，包括文本分析、图像生成、配音生成和角色管理等功能。

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

# 仅测试文本分析流程
python3 test_ai_service_workflow.py --test text
```

**测试内容:**
- ✅ 调用七牛 AI 推理 API (DeepSeek-V3)
- ✅ 分析小说文本
- ✅ 生成场景列表
- ✅ 识别角色
- ✅ 归一化角色描述

**预期输出:**
```
📖 测试文本分析流程 (小说文本 → 场景和角色信息)
============================================================
📝 输入文本长度: 234 字符
🔄 正在执行文本分析流程...

✅ 文本分析流程完成！生成了 2 个场景

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

# 仅测试图像生成流程
python3 test_ai_service_workflow.py --test image
```

---

### 步骤 3.5: 功能测试 - 配音生成

测试七牛云 TTS：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service

# 仅测试配音生成流程
python3 test_ai_service_workflow.py --test voice
```

**测试内容 (配音生成):**
- ✅ 测试女声配音
- ✅ 测试男声配音
- ✅ 测试童声配音
- ✅ 验证音频时长计算
- ✅ 保存音频到本地

**预期输出:**
```
🎙️  测试配音生成流程 (文本 → 语音文件)
============================================================
🎵 流程测试 1: 女声配音生成
输入: 文本 + 女声参数 → 输出: 女声语音文件
文本: 春天的早晨，校园里樱花盛开...
✅ 女声配音生成完成
   文件路径: /tmp/tfboys/audio/test_task/scene_001.mp3
   时长: 5.42 秒
   文件大小: 87.23 KB
```

---

### 步骤 3.6: 功能测试 - 角色管理

测试角色去重和 Redis 缓存：

```bash
cd /Users/jiangzhi/repo/tfboys/backend/ai-service

# 仅测试角色管理流程
python3 test_ai_service_workflow.py --test character
```

**测试内容 (角色管理):**
- ✅ 角色 ID 生成 (基于名称 hash)
- ✅ 角色去重逻辑
- ✅ 角色设定图生成
- ✅ Redis 缓存存取
- ✅ 批量角色处理
- ✅ 任务角色关联

**预期输出:**
```
👥 测试角色管理流程 (角色去重、设定图生成、缓存管理)
============================================================
🔑 测试 1: 角色 ID 生成
小明 ID: char_12345678
✅ 同名角色 ID 一致

🎨 测试 2: 创建角色并生成设定图
✅ 角色创建成功
   角色名称: 测试角色小明
   设定图路径: /tmp/tfboys/characters/测试角色小明.png

💾 测试 3: 从 Redis 缓存获取角色
✅ 角色从缓存获取成功（ID 一致）
✅ 设定图复用成功（URL 一致）

📋 测试 4: 批量处理场景中的角色
✅ 角色处理完成
   去重后角色数: 3
   ✅ 角色去重正确（预期 3 个角色：A、B、C）
```

---

### 步骤 3 测试内容总结

**图像生成测试:**
- ✅ 生成角色设定图
- ✅ 生成场景图像
- ✅ 测试不同宽高比 (1:1, 16:9, 9:16)
- ✅ 保存图像到本地

**图像生成预期输出:**
```
🎨 测试图像生成流程 (角色和场景 → 图像文件)
============================================================
📸 流程测试 1: 角色设定图生成
输入: 角色描述 → 输出: 角色设定图
角色: 小明 (黑色短发，蓝色眼睛的少年)
✅ 角色设定图生成完成: /tmp/tfboys/characters/小明.png
   文件大小: 245.67 KB

📸 流程测试 2: 场景图像生成
输入: 场景描述 + 角色上下文 → 输出: 场景图像
场景: 春天的校园，樱花飘落
✅ 场景图像生成完成: /tmp/tfboys/scenes/test_scene_001.png
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

# 测试完整工作流程
python3 test_ai_service_workflow.py --test all
```

---

### 步骤 5: 启动服务进行端到端测试

启动 AI Service 并通过 API 端点测试：

```bash
cd backend/ai-service

# 设置项目根目录到 PYTHONPATH
export PYTHONPATH="$(cd ../.. && pwd)"

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**注意:** 由于 ai-service 依赖项目根目录的 `shared` 模块，启动时必须设置 `PYTHONPATH` 环境变量指向项目根目录。

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
export PYTHONPATH="$(cd ../.. && pwd)"
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

---

## 📊 测试检查清单

### 文本分析功能
- [ ] 单元测试通过
- [ ] 功能测试成功调用七牛 API (DeepSeek-V3)
- [ ] 成功生成场景列表
- [ ] 角色识别正确
- [ ] 场景描述合理

### 图像生成功能
- [ ] 单元测试部分通过
- [ ] 功能测试成功生成角色图
- [ ] 功能测试成功生成场景图
- [ ] 不同宽高比都能生成 (1:1, 16:9, 9:16)
- [ ] 图像文件正常保存

### 配音生成功能
- [ ] 功能测试成功生成女声配音
- [ ] 功能测试成功生成男声配音
- [ ] 功能测试成功生成童声配音
- [ ] 音频时长计算正确
- [ ] 音频文件正常保存

### 角色管理功能
- [ ] 角色 ID 生成一致性正确
- [ ] 角色去重逻辑正确
- [ ] 角色设定图生成成功
- [ ] Redis 缓存存取正常
- [ ] 批量角色处理正确
- [ ] 任务角色关联正确

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
time python3 test_ai_service_workflow.py --test text

# 测试图像生成性能
time python3 test_ai_service_workflow.py --test image
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

### 核心功能测试
1. ✅ 单元测试: 文本分析 7/7 通过
2. ✅ 功能测试: 文本分析成功 (DeepSeek-V3)
3. ✅ 功能测试: 图像生成成功 (七牛文生图 API)
4. ✅ 功能测试: 配音生成成功 (七牛云 TTS) - 可选
5. ✅ 功能测试: 角色管理成功 (去重+缓存+图像)

### 服务集成测试
6. ✅ 服务启动: 无错误
7. ✅ API 调用: 正常响应
8. ✅ 生成结果: 质量符合预期

### 快速测试命令
```bash
# 测试所有核心功能（不含配音）
python3 test_ai_service_workflow.py --test text
python3 test_ai_service_workflow.py --test image
python3 test_ai_service_workflow.py --test character

# 测试完整工作流程（包含配音，需配置 TTS 密钥）
python3 test_ai_service_workflow.py --test all
```

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
