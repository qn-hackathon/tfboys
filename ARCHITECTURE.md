# 文字生成视频系统 - 模块架构设计

## 1. 系统架构概览

```
┌─────────────┐
│   前端层    │  (Web UI)
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────────┐
│           API Gateway                    │
└─────┬───────────────────────┬───────────┘
      │                       │
      ▼                       ▼
┌─────────────┐       ┌─────────────┐
│  AI处理服务  │       │ 视频合成服务 │
│  (Worker)   │◄─────►│  (Worker)   │
└─────────────┘       └─────────────┘
      │                       │
      ▼                       ▼
┌─────────────────────────────────────────┐
│         共享存储 (OSS + Redis)           │
└─────────────────────────────────────────┘
```

---

## 2. 模块拆分与职责

### 模块1: 前端服务 (Frontend Service)

**负责人**: 前端工程师

**核心职责**:
- 用户界面展示
- 文件上传(小说文本)
- 任务提交与状态监控
- 视频预览与下载

**技术栈**:
- React/Vue.js + TypeScript
- Ant Design / Element UI
- Axios (HTTP客户端)

**基本原理**:
```
用户操作 → 表单验证 → HTTP请求 → 轮询任务状态 → 显示结果
```

---

### 模块2: AI处理服务 (AI Processing Service)

**负责人**: AI工程师

**核心职责**:
- 文本分析与场景分割
- 角色识别与设定
- 图像生成(调用Midjourney)
- 配音生成(调用阿里云TTS)
- 角色一致性管理

**技术栈**:
- Python + FastAPI
- OpenAI SDK / Anthropic SDK
- Midjourney API客户端
- 阿里云TTS SDK
- Celery (异步任务队列)

**基本原理**:
```
接收任务 
  → 文本分析(GPT-4/Claude) 
    → 场景分割 + 角色提取
  → 图像生成(Midjourney + --cref)
    → 首次角色: 生成角色设定图
    → 后续场景: 引用角色图生成
  → 配音生成(阿里云TTS)
    → 为每个场景生成旁白/对话
  → 输出: 场景数据包(图片URL + 音频URL + 文本)
```

**角色一致性实现**:
1. 第一次出现角色时,生成"角色设定图"
2. 保存角色图到角色库(OSS)
3. 后续场景使用Midjourney的`--cref <角色图URL>`参数
4. 维护角色ID与图片URL的映射关系

---

### 模块3: 视频合成服务 (Video Synthesis Service)

**负责人**: 视频工程师

**核心职责**:
- 接收场景数据包
- 使用FFmpeg合成视频
- 字幕叠加
- 音频同步
- 场景拼接
- 输出最终视频

**技术栈**:
- Python + FastAPI
- FFmpeg
- Pillow (图像处理)
- Celery (异步任务队列)

**基本原理**:
```
接收场景数据包
  → 下载图片和音频资源
  → FFmpeg处理单个场景:
    - 图片 + 字幕叠加
    - 图片 + 音频同步(图片持续时间=音频时长)
  → FFmpeg场景拼接:
    - concat协议连接所有场景
  → 添加转场效果(可选)
  → 输出最终MP4视频
  → 上传到OSS
```

**FFmpeg关键命令**:
```bash
# 单场景合成(图+音+字幕)
ffmpeg -loop 1 -i scene.jpg -i audio.mp3 \
  -vf "drawtext=..." -shortest scene.mp4

# 多场景拼接
ffmpeg -f concat -i scenes.txt -c copy final.mp4
```

---

## 3. 数据流图

```
用户上传小说
    ↓
[前端] POST /tasks → [AI服务] 创建任务
    ↓
[AI服务] 文本分析 → Redis写入任务状态
    ↓
[AI服务] 图像生成 → OSS保存图片
    ↓
[AI服务] 配音生成 → OSS保存音频
    ↓
[AI服务] 发送场景数据 → [视频服务]
    ↓
[视频服务] FFmpeg合成 → OSS保存视频
    ↓
[视频服务] 更新任务状态 → Redis
    ↓
[前端] 轮询任务状态 → 显示下载链接
```

---

## 4. 核心数据结构

### 任务对象 (Task)
```json
{
  "task_id": "uuid",
  "status": "pending|processing|completed|failed",
  "novel_text": "小说内容...",
  "created_at": "2025-10-24T08:00:00Z",
  "progress": {
    "total_scenes": 10,
    "processed_scenes": 3
  },
  "result": {
    "video_url": "https://oss.example.com/videos/xxx.mp4"
  }
}
```

### 场景对象 (Scene)
```json
{
  "scene_id": "uuid",
  "scene_index": 1,
  "description": "场景描述文本",
  "narration": "旁白文字",
  "characters": [
    {
      "character_id": "char_001",
      "name": "主角",
      "reference_image_url": "https://oss.example.com/characters/char_001.jpg"
    }
  ],
  "image_url": "https://oss.example.com/scenes/scene_001.jpg",
  "audio_url": "https://oss.example.com/audio/scene_001.mp3",
  "duration": 5.2
}
```

### 角色对象 (Character)
```json
{
  "character_id": "char_001",
  "name": "主角",
  "description": "少年,黑色短发,蓝色眼睛,校服",
  "reference_image_url": "https://oss.example.com/characters/char_001.jpg",
  "midjourney_cref_url": "https://oss.example.com/characters/char_001.jpg"
}
```

---

## 5. 技术难点与解决方案

### 难点1: 角色一致性
**解决方案**: 
- 使用Midjourney的`--cref`参数
- 维护角色库,首次生成后复用
- 角色ID与参考图URL的强关联

### 难点2: 异步任务管理
**解决方案**:
- Celery + Redis实现任务队列
- 任务状态实时更新到Redis
- 前端轮询或WebSocket推送

### 难点3: 视频合成性能
**解决方案**:
- 异步处理,避免阻塞
- 场景并行生成(AI服务)
- FFmpeg硬件加速(GPU)

### 难点4: 大模型调用限流
**解决方案**:
- 实现重试机制
- 队列削峰
- 多账号轮询(如果需要)

---

## 6. 扩展性考虑

### 水平扩展
- AI服务和视频服务均可多实例部署
- 通过Celery分布式任务队列负载均衡

### 功能扩展
- 支持多种配音风格(通过TTS参数)
- 支持自定义角色设定图上传
- 支持视频风格切换(写实/动漫/水墨等)
- 集成视频动态化(Runway Gen-2等)

---

## 7. 部署架构

```
┌────────────────────────────────────────┐
│         Nginx (负载均衡)               │
└───────┬────────────────────────────────┘
        │
        ├─► [前端静态资源] (CDN)
        │
        ├─► [API Gateway] (容器 x 2)
        │
        ├─► [AI服务] (容器 x 4, GPU可选)
        │
        └─► [视频服务] (容器 x 2, GPU推荐)

共享层:
  - Redis (任务队列 + 缓存)
  - OSS (文件存储)
  - RDS (元数据,可选)
```

---

## 8. 开发优先级

### P0 (第1天)
1. AI服务: 文本分析 + 图像生成
2. 前端: 任务提交 + 状态查询

### P1 (第2天上午)
3. AI服务: 配音生成
4. 视频服务: 基础合成

### P2 (第2天下午)
5. 视频服务: 字幕叠加 + 优化
6. 前端: 视频预览

---

## 9. 风险与应对

| 风险 | 应对措施 |
|------|---------|
| Midjourney API限流 | 降低并发数,实现队列排队 |
| FFmpeg合成慢 | 启用GPU加速,优化参数 |
| 大模型输出不稳定 | 多次重试 + Prompt工程优化 |
| 角色一致性不佳 | 调整--cw参数,优化角色描述 |

---

**下一步**: 查看 `API.md` 了解详细的接口定义。
