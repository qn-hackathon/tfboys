# 文字生成视频系统 - API接口定义

## 接口规范说明

- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **认证**: Bearer Token (可选)
- **基础URL**: `https://api.example.com/v1`

---

## 1. 前端 ↔ AI处理服务

前端工程师直接调用这些接口来提交任务和获取状态。

### 1.1 创建视频生成任务

**接口**: `POST /tasks`

**描述**: 用户上传小说文本,创建视频生成任务

**请求体**:
```json
{
  "novel_text": "这是小说的完整文本内容...",
  "options": {
    "video_style": "anime",
    "voice_type": "female",
    "video_resolution": "1080p"
  }
}
```

**响应**: `201 Created`
```json
{
  "code": 0,
  "message": "任务创建成功",
  "data": {
    "task_id": "task_abc123",
    "status": "pending",
    "created_at": "2025-10-24T08:00:00Z",
    "estimated_time": 300
  }
}
```

**错误响应**: `400 Bad Request`
```json
{
  "code": 40001,
  "message": "小说文本不能为空"
}
```

---

### 1.2 查询任务状态

**接口**: `GET /tasks/{task_id}`

**描述**: 轮询查询任务处理状态和进度

**响应**: `200 OK`
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "task_id": "task_abc123",
    "status": "processing",
    "progress": {
      "current_stage": "generating_images",
      "total_scenes": 10,
      "processed_scenes": 5,
      "percentage": 50
    },
    "created_at": "2025-10-24T08:00:00Z",
    "updated_at": "2025-10-24T08:05:00Z"
  }
}
```

**任务完成时的响应**:
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "task_id": "task_abc123",
    "status": "completed",
    "progress": {
      "percentage": 100
    },
    "result": {
      "video_url": "https://oss.example.com/videos/task_abc123.mp4",
      "duration": 120.5,
      "scenes_count": 10,
      "thumbnail_url": "https://oss.example.com/thumbnails/task_abc123.jpg"
    },
    "created_at": "2025-10-24T08:00:00Z",
    "completed_at": "2025-10-24T08:10:00Z"
  }
}
```

**任务失败时的响应**:
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "task_id": "task_abc123",
    "status": "failed",
    "error": {
      "code": 50001,
      "message": "图像生成失败: Midjourney API限流",
      "retry_able": true
    }
  }
}
```

---

### 1.3 获取任务列表

**接口**: `GET /tasks?page=1&page_size=10&status=completed`

**描述**: 获取用户的任务历史列表

**响应**: `200 OK`
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "total": 25,
    "page": 1,
    "page_size": 10,
    "tasks": [
      {
        "task_id": "task_abc123",
        "status": "completed",
        "created_at": "2025-10-24T08:00:00Z",
        "video_url": "https://oss.example.com/videos/task_abc123.mp4"
      }
    ]
  }
}
```

---

### 1.4 取消任务

**接口**: `DELETE /tasks/{task_id}`

**描述**: 取消正在处理的任务

**响应**: `200 OK`
```json
{
  "code": 0,
  "message": "任务已取消"
}
```

---

## 2. AI处理服务 ↔ 视频合成服务

AI处理服务生成场景数据后,通过内部API传递给视频合成服务。

### 2.1 提交场景数据包

**接口**: `POST /internal/video-synthesis/jobs`

**描述**: AI服务完成场景分析、图像和配音生成后,提交场景数据给视频服务

**请求体**:
```json
{
  "task_id": "task_abc123",
  "scenes": [
    {
      "scene_id": "scene_001",
      "scene_index": 1,
      "description": "清晨的校园,樱花飘落",
      "narration": "春天的早晨,校园里樱花盛开。",
      "characters": [
        {
          "character_id": "char_001",
          "name": "主角",
          "reference_image_url": "https://oss.example.com/characters/char_001.jpg"
        }
      ],
      "image_url": "https://oss.example.com/scenes/scene_001.jpg",
      "audio_url": "https://oss.example.com/audio/scene_001.mp3",
      "audio_duration": 5.2,
      "subtitle_text": "春天的早晨,校园里樱花盛开。"
    },
    {
      "scene_id": "scene_002",
      "scene_index": 2,
      "description": "教室内,学生们在讨论",
      "narration": "同学们热烈地讨论着即将到来的考试。",
      "characters": [
        {
          "character_id": "char_001",
          "name": "主角"
        },
        {
          "character_id": "char_002",
          "name": "同学A",
          "reference_image_url": "https://oss.example.com/characters/char_002.jpg"
        }
      ],
      "image_url": "https://oss.example.com/scenes/scene_002.jpg",
      "audio_url": "https://oss.example.com/audio/scene_002.mp3",
      "audio_duration": 6.8,
      "subtitle_text": "同学们热烈地讨论着即将到来的考试。"
    }
  ],
  "video_config": {
    "resolution": "1920x1080",
    "fps": 30,
    "transition_effect": "fade",
    "subtitle_style": {
      "font": "Arial",
      "font_size": 24,
      "color": "white",
      "position": "bottom"
    }
  }
}
```

**响应**: `201 Created`
```json
{
  "code": 0,
  "message": "视频合成任务已创建",
  "data": {
    "job_id": "video_job_xyz789",
    "task_id": "task_abc123",
    "status": "pending",
    "estimated_time": 60
  }
}
```

---

### 2.2 查询视频合成状态

**接口**: `GET /internal/video-synthesis/jobs/{job_id}`

**描述**: AI服务或主服务查询视频合成进度

**响应**: `200 OK`
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "job_id": "video_job_xyz789",
    "task_id": "task_abc123",
    "status": "processing",
    "progress": {
      "current_scene": 5,
      "total_scenes": 10,
      "percentage": 50
    }
  }
}
```

**合成完成时的响应**:
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "job_id": "video_job_xyz789",
    "task_id": "task_abc123",
    "status": "completed",
    "result": {
      "video_url": "https://oss.example.com/videos/task_abc123.mp4",
      "duration": 120.5,
      "file_size": 45678900,
      "thumbnail_url": "https://oss.example.com/thumbnails/task_abc123.jpg"
    }
  }
}
```

---

### 2.3 视频合成完成回调 (可选)

**接口**: `POST /ai-service/callbacks/video-completed`

**描述**: 视频服务合成完成后,回调AI服务(或主服务)更新任务状态

**请求体**:
```json
{
  "job_id": "video_job_xyz789",
  "task_id": "task_abc123",
  "status": "completed",
  "video_url": "https://oss.example.com/videos/task_abc123.mp4",
  "duration": 120.5
}
```

**响应**: `200 OK`
```json
{
  "code": 0,
  "message": "回调接收成功"
}
```

---

## 3. 共享数据存储

所有服务共享Redis和OSS,以下是数据结构约定。

### 3.1 Redis任务状态存储

**Key**: `task:{task_id}`

**Value** (JSON):
```json
{
  "task_id": "task_abc123",
  "status": "processing",
  "progress": {
    "current_stage": "generating_images",
    "total_scenes": 10,
    "processed_scenes": 5
  },
  "created_at": "2025-10-24T08:00:00Z",
  "updated_at": "2025-10-24T08:05:00Z"
}
```

**TTL**: 7天

---

### 3.2 Redis角色库存储

**Key**: `character:{character_id}`

**Value** (JSON):
```json
{
  "character_id": "char_001",
  "name": "主角",
  "description": "少年,黑色短发,蓝色眼睛,校服",
  "reference_image_url": "https://oss.example.com/characters/char_001.jpg",
  "created_at": "2025-10-24T08:00:00Z"
}
```

**TTL**: 永久

---

### 3.3 OSS文件存储路径规范

```
bucket/
├── characters/          # 角色设定图
│   ├── char_001.jpg
│   └── char_002.jpg
├── scenes/              # 场景图片
│   ├── task_abc123/
│   │   ├── scene_001.jpg
│   │   └── scene_002.jpg
├── audio/               # 配音文件
│   ├── task_abc123/
│   │   ├── scene_001.mp3
│   │   └── scene_002.mp3
├── videos/              # 最终视频
│   └── task_abc123.mp4
└── thumbnails/          # 视频缩略图
    └── task_abc123.jpg
```

---

## 4. 错误码定义

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 40001 | 请求参数错误 |
| 40101 | 认证失败 |
| 40401 | 资源不存在 |
| 42901 | 请求过于频繁 |
| 50001 | 第三方API调用失败 |
| 50002 | 文件处理失败 |
| 50003 | 数据库错误 |
| 50099 | 未知服务器错误 |

---

## 5. 任务状态枚举

| 状态 | 说明 |
|------|------|
| pending | 任务已创建,等待处理 |
| analyzing | 文本分析中 |
| generating_images | 图像生成中 |
| generating_audio | 配音生成中 |
| synthesizing_video | 视频合成中 |
| completed | 任务完成 |
| failed | 任务失败 |
| cancelled | 任务已取消 |

---

## 6. 3人协作接口调用流程示例

### 场景: 用户提交小说生成视频

```
┌─────────┐         ┌─────────┐         ┌─────────┐
│  前端   │         │ AI服务  │         │ 视频服务│
└────┬────┘         └────┬────┘         └────┬────┘
     │                   │                   │
     │ 1. POST /tasks    │                   │
     │──────────────────>│                   │
     │                   │                   │
     │ 2. 201 Created    │                   │
     │<──────────────────│                   │
     │   {task_id}       │                   │
     │                   │                   │
     │ 3. 轮询状态       │                   │
     │ GET /tasks/{id}   │                   │
     │──────────────────>│                   │
     │                   │                   │
     │                   │ 4. 文本分析       │
     │                   │    图像生成       │
     │                   │    配音生成       │
     │                   │                   │
     │ 5. 返回进度       │                   │
     │<──────────────────│                   │
     │   {processing}    │                   │
     │                   │                   │
     │                   │ 6. POST /internal/│
     │                   │    video-synthesis│
     │                   │───────────────────>│
     │                   │                   │
     │                   │ 7. 201 Created    │
     │                   │<───────────────────│
     │                   │   {job_id}        │
     │                   │                   │
     │                   │                   │ 8. FFmpeg合成
     │                   │                   │
     │                   │ 9. 回调           │
     │                   │<───────────────────│
     │                   │   {video_url}     │
     │                   │                   │
     │10. 轮询状态       │                   │
     │ GET /tasks/{id}   │                   │
     │──────────────────>│                   │
     │                   │                   │
     │11. 返回完成       │                   │
     │<──────────────────│                   │
     │   {completed,     │                   │
     │    video_url}     │                   │
     │                   │                   │
```

---

## 7. 测试用例

### 7.1 前端测试清单

- [ ] 创建任务 - 正常流程
- [ ] 创建任务 - 空文本错误
- [ ] 查询任务 - 处理中状态
- [ ] 查询任务 - 完成状态
- [ ] 查询任务 - 失败状态
- [ ] 轮询频率控制(建议5秒)

### 7.2 AI服务测试清单

- [ ] 接收任务并解析文本
- [ ] 场景分割准确性
- [ ] 角色提取与一致性
- [ ] Midjourney图像生成
- [ ] TTS配音生成
- [ ] 提交场景数据给视频服务

### 7.3 视频服务测试清单

- [ ] 接收场景数据包
- [ ] 单场景视频合成
- [ ] 多场景拼接
- [ ] 字幕叠加
- [ ] 视频上传OSS

---

## 8. 接口Mock数据(开发阶段)

为了让3人并行开发,可以先使用Mock数据:

### 前端Mock
```javascript
// Mock创建任务响应
{
  code: 0,
  message: "任务创建成功",
  data: {
    task_id: "mock_task_001",
    status: "pending"
  }
}
```

### AI服务Mock
```python
# Mock场景数据
mock_scenes = [
    {
        "scene_id": "scene_001",
        "scene_index": 1,
        "image_url": "https://via.placeholder.com/1920x1080",
        "audio_url": "https://example.com/sample.mp3",
        "audio_duration": 5.0,
        "subtitle_text": "测试字幕"
    }
]
```

### 视频服务Mock
```python
# Mock视频合成结果
mock_result = {
    "job_id": "mock_job_001",
    "status": "completed",
    "video_url": "https://example.com/sample.mp4"
}
```

---

## 9. 部署与联调

### 本地开发环境
- 前端: `http://localhost:3000`
- AI服务: `http://localhost:8001`
- 视频服务: `http://localhost:8002`
- Redis: `localhost:6379`

### 联调顺序
1. **Day 1上午**: 前端 + AI服务Mock联调
2. **Day 1下午**: AI服务 + 视频服务Mock联调
3. **Day 2上午**: 三方集成联调
4. **Day 2下午**: 完整流程测试

---

## 10. API文档工具推荐

- **Swagger/OpenAPI**: 自动生成API文档
- **Postman**: 接口测试
- **Apifox**: 国产接口管理工具

---

**完成标志**: 所有接口按照此规范实现后,三方服务可以独立开发、并行测试。
