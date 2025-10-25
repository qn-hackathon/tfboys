# AI Service 模块依赖关系文档

本文档描述 AI Service 中 `workers/tasks.py` 模块与其他服务模块的调用关系和接口定义。

## 文档版本

- **版本**: 1.0
- **最后更新**: 2024-10-25
- **维护者**: TFBoys Team

---

## 一、模块职责

`backend/ai-service/app/workers/tasks.py` 是 AI Service 的 **Celery 异步任务处理核心**,负责编排整个视频生成流程:

```
process_novel_task(task_id, novel_text)
  ↓
1. 调用 text_analyzer → 获取场景列表
2. 调用 character_manager + image_generator → 生成角色设定图
3. 调用 image_generator → 生成场景图(使用--cref)
4. 调用 voice_generator → 生成配音
5. 调用 video_client → 提交视频合成任务
6. 全程更新 redis_client → 任务状态同步
```

---

## 二、本模块直接调用的服务

### 1️⃣ TextAnalyzer (文本分析服务)

**模块类型**: 同服务内模块  
**位置**: `backend/ai-service/app/services/text_analyzer.py`

#### 调用方法

```python
from app.services.text_analyzer import text_analyzer

scenes_data = text_analyzer.analyze_novel(novel_text: str) -> List[Dict]
```

#### 输入参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `novel_text` | str | 小说文本内容 |

#### 输出格式

返回 `List[Dict]`,每个场景包含:

```python
[
    {
        "scene_index": 1,                              # 场景索引
        "description": "清晨的校园,樱花飘落",           # 场景描述(用于图像生成)
        "narration": "春天的早晨,校园里樱花盛开。",     # 旁白文字(用于配音)
        "characters": [                                # 场景中出现的角色
            {
                "name": "主角",                        # 角色名称
                "description": "少年,黑色短发,蓝色眼睛,校服"  # 角色外貌特征
            }
        ]
    },
    ...
]
```

#### 相关文档

- **实现逻辑**: CLAUDE.md 第71-82行 "AI处理服务基本原理"
- **API规范**: docs/API.md

---

### 2️⃣ ImageGenerator (图像生成服务)

**模块类型**: 同服务内模块  
**位置**: `backend/ai-service/app/services/image_generator.py`

#### 调用方法

```python
from app.services.image_generator import image_generator

# 生成角色设定图(无--cref)
character_ref_url = await image_generator.generate_image(
    prompt="anime style, character design sheet, 主角, 黑色短发, --ar 1:1",
    character_ref_url=None,
    ar="1:1"
)

# 生成场景图(使用--cref)
scene_image_url = await image_generator.generate_image(
    prompt="anime style, 清晨的校园,樱花飘落 --niji 6",
    character_ref_url="https://oss.example.com/characters/char_001.jpg",
    ar="16:9"
)
```

#### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `prompt` | str | 是 | - | Midjourney 提示词 |
| `character_ref_url` | str | 否 | None | 角色参考图 URL (用于 `--cref` 参数) |
| `ar` | str | 否 | "16:9" | 宽高比 |

#### 输出格式

返回 `str`: 生成的图像 URL (OSS 存储路径)

#### 实现细节

- 内部调用 Midjourney API (第三方服务,非本模块直接调用)
- 返回已上传到 OSS 的图像 URL
- 使用 `--cref` 参数确保角色一致性

#### 相关文档

- **角色一致性**: CLAUDE.md 第84-88行 "角色一致性实现"
- **API示例**: docs/API.md 第178-237行 "提交场景数据包"

---

### 3️⃣ VoiceGenerator (配音生成服务)

**模块类型**: 同服务内模块  
**位置**: `backend/ai-service/app/services/voice_generator.py`

#### 调用方法

```python
from app.services.voice_generator import voice_generator

audio_url = await voice_generator.generate_voice(
    text="春天的早晨,校园里樱花盛开。",
    voice="zhiyan"  # 阿里云 TTS 音色代码
)
```

#### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `text` | str | 是 | - | 配音文字内容 |
| `voice` | str | 否 | "zhiyan" | 音色类型 |

#### 输出格式

返回 `str`: 生成的音频文件 URL (OSS 存储路径)

- **音频格式**: MP3
- **音频时长**: 需从阿里云 TTS 响应中获取

#### 实现细节

- 内部调用阿里云 TTS SDK (第三方服务,非本模块直接调用)
- 返回已上传到 OSS 的音频 URL

#### 相关文档

- **OSS路径规范**: docs/API.md 第384-392行 "OSS文件存储路径规范"

---

### 4️⃣ CharacterManager (角色管理服务)

**模块类型**: 同服务内模块  
**位置**: `backend/ai-service/app/services/character_manager.py`

#### 调用方法

```python
from app.services.character_manager import character_manager

# 保存角色到 Redis
await character_manager.save_character(
    task_id="task_abc123",
    character_name="主角",
    character_data={
        "character_id": "char_001",
        "name": "主角",
        "description": "少年,黑色短发,蓝色眼睛,校服",
        "reference_image_url": "https://oss.example.com/characters/char_001.jpg"
    }
)

# 获取角色信息
character = await character_manager.get_character(
    task_id="task_abc123",
    character_name="主角"
)
```

#### 方法: save_character

**输入参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `task_id` | str | 任务ID |
| `character_name` | str | 角色名称 |
| `character_data` | Dict | 角色数据 |

**返回**: None

#### 方法: get_character

**输入参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `task_id` | str | 任务ID |
| `character_name` | str | 角色名称 |

**返回**: `Optional[Dict]` - 角色数据,不存在返回 None

#### 数据存储

**Redis Key**: `character:{task_id}:{character_name}`

#### 相关文档

- **Character模型**: shared/models/scene.py 第9-17行
- **Redis存储规范**: docs/API.md 第354-370行 "Redis角色库存储"

---

### 5️⃣ VideoClient (视频服务客户端)

**模块类型**: 同服务内模块 (HTTP 客户端)  
**位置**: `backend/ai-service/app/services/video_client.py`

#### 调用方法

```python
from app.services.video_client import video_client
from shared.models import Scene

# 提交视频合成任务
job_id = await video_client.submit_video_synthesis_job(
    task_id="task_abc123",
    scenes=[
        Scene(
            scene_id="scene_001",
            scene_index=1,
            description="清晨的校园,樱花飘落",
            narration="春天的早晨,校园里樱花盛开。",
            characters=[...],
            image_url="https://oss.example.com/scenes/scene_001.jpg",
            audio_url="https://oss.example.com/audio/scene_001.mp3",
            duration=5.2
        ),
        ...
    ]
)
```

#### 输入参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `task_id` | str | 任务ID |
| `scenes` | List[Scene] | 场景列表 (使用 shared.models.Scene 模型) |

#### 输出格式

返回 `str`: 视频合成任务ID (job_id)

#### HTTP 请求详情

- **目标服务**: Video Service
- **接口**: `POST /internal/video-synthesis/jobs`
- **请求体**: 参考 docs/API.md 第180-237行
- **响应**: 参考 docs/API.md 第239-251行

#### 相关文档

- **客户端实现**: backend/ai-service/app/services/video_client.py 第29-71行
- **服务端接口**: backend/video-service/app/api/internal.py 第35-67行
- **API规范**: docs/API.md 第175-251行 "AI处理服务 ↔ 视频合成服务"

---

### 6️⃣ RedisClient (Redis客户端)

**模块类型**: 共享模块  
**位置**: `shared/clients/redis_client.py`

#### 调用方法

```python
from shared.clients import redis_client
from shared.enums import TaskStatus

# 保存任务
await redis_client.save_task(
    task_id="task_abc123",
    task_data={
        "task_id": "task_abc123",
        "status": TaskStatus.ANALYZING.value,
        "novel_text": "...",
        "scenes": [...],
        "progress": {
            "current_step": "analyzing",
            "total_scenes": 10,
            "processed_scenes": 3,
            "percentage": 30
        }
    },
    ttl=604800  # 7天
)

# 获取任务
task_data = await redis_client.get_task(task_id="task_abc123")

# 更新任务状态
await redis_client.update_task_status(
    task_id="task_abc123",
    status=TaskStatus.GENERATING_IMAGES.value,
    error=None
)
```

#### 主要方法

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `save_task` | task_id, task_data, ttl | None | 保存任务数据 |
| `get_task` | task_id | Optional[dict] | 获取任务数据 |
| `update_task_status` | task_id, status, error | None | 更新任务状态 |

#### 数据存储

**Redis Key**: `task:{task_id}`  
**TTL**: 默认 7天 (604800秒)

#### 相关文档

- **客户端实现**: shared/clients/redis_client.py 第24-79行
- **TaskStatus枚举**: shared/enums.py 第7-14行
- **存储规范**: docs/API.md 第331-351行 "Redis任务状态存储"

---

## 三、不在本模块直接调用的服务

以下服务由上述模块内部调用,**不需要** tasks.py 直接关心:

### ❌ OpenAI GPT-4

- **调用者**: TextAnalyzer
- **用途**: 文本分析、场景分割、角色识别
- **API文档**: https://platform.openai.com/docs/api-reference

### ❌ Midjourney API

- **调用者**: ImageGenerator
- **用途**: 生成动漫风格图像
- **API文档**: https://docs.midjourney.com/
- **第三方服务**: https://www.midjourneyapi.io/

### ❌ 阿里云 TTS

- **调用者**: VoiceGenerator
- **用途**: 生成中文配音
- **SDK**: alibabacloud-nls-python-sdk
- **API文档**: https://help.aliyun.com/document_detail/84435.html

### ❌ 阿里云 OSS

- **调用者**: ImageGenerator, VoiceGenerator
- **用途**: 存储图像和音频文件
- **SDK**: oss2
- **API文档**: https://help.aliyun.com/product/31815.html

---

## 四、数据流图

```
API Gateway
    │
    ├──► POST /internal/tasks
    │       ↓
    │   [AI Service] 创建任务 → Redis (status: pending)
    │       ↓
    │   [Celery Worker] process_novel_task
    │       ↓
    ├──► text_analyzer.analyze_novel()
    │       ↓ (scenes_data: List[Dict])
    │
    ├──► image_generator.generate_image() (角色设定图)
    │       ↓ (character_ref_url)
    │
    ├──► character_manager.save_character() → Redis
    │
    ├──► image_generator.generate_image() (场景图 + --cref)
    │       ↓ (scene_image_url)
    │
    ├──► voice_generator.generate_voice()
    │       ↓ (audio_url)
    │
    ├──► video_client.submit_video_synthesis_job()
    │       ↓ HTTP POST → [Video Service]
    │           ↓
    │       [Video Service] FFmpeg 合成
    │           ↓
    │       回调 AI Service → Redis (status: completed)
    │
    └──► 前端轮询 GET /tasks/{task_id} → 获取 video_url
```

---

## 五、实现示例

### 完整的任务处理流程

```python
from app.workers.celery_app import celery_app
from app.services.text_analyzer import text_analyzer
from app.services.image_generator import image_generator
from app.services.voice_generator import voice_generator
from app.services.character_manager import character_manager
from app.services.video_client import video_client
from shared.clients import redis_client
from shared.models import Scene, Character
from shared.enums import TaskStatus
import asyncio


@celery_app.task(name="process_novel_task")
def process_novel_task(task_id: str, novel_text: str):
    """处理小说生成视频任务(Celery 入口)"""
    return asyncio.run(_process_novel_task_async(task_id, novel_text))


async def _process_novel_task_async(task_id: str, novel_text: str):
    """
    异步处理流程
    
    步骤:
    1. 文本分析 → 获取场景列表
    2. 角色处理 → 生成角色设定图 + 保存到 Redis
    3. 场景处理 → 生成场景图(--cref) + 配音
    4. 提交视频服务 → 调用 video_client
    5. 全程更新任务状态到 Redis
    """
    try:
        # === 步骤1: 文本分析 ===
        await redis_client.update_task_status(task_id, TaskStatus.ANALYZING.value)
        
        scenes_data = text_analyzer.analyze_novel(novel_text)
        total_scenes = len(scenes_data)
        
        # === 步骤2: 角色处理 ===
        characters_map = {}
        
        for scene_data in scenes_data:
            for char_data in scene_data["characters"]:
                char_name = char_data["name"]
                
                if char_name not in characters_map:
                    # 首次出现:生成角色设定图
                    char_prompt = f"anime style, character design sheet, {char_name}, {char_data['description']}"
                    char_ref_url = await image_generator.generate_image(
                        prompt=char_prompt,
                        character_ref_url=None,
                        ar="1:1"
                    )
                    
                    # 保存角色到 Redis
                    character = Character(
                        character_id=f"char_{task_id}_{char_name}",
                        name=char_name,
                        description=char_data["description"],
                        reference_image_url=char_ref_url,
                        midjourney_cref_url=char_ref_url
                    )
                    characters_map[char_name] = character
                    
                    await character_manager.save_character(
                        task_id=task_id,
                        character_name=char_name,
                        character_data=character.model_dump()
                    )
        
        # === 步骤3: 场景处理 ===
        await redis_client.update_task_status(task_id, TaskStatus.GENERATING_IMAGES.value)
        
        scenes = []
        for idx, scene_data in enumerate(scenes_data):
            scene_id = f"scene_{task_id}_{idx:03d}"
            
            # 3.1 生成场景图(使用--cref)
            main_char = scene_data["characters"][0] if scene_data["characters"] else None
            char_ref_url = characters_map[main_char["name"]].reference_image_url if main_char else None
            
            scene_image_url = await image_generator.generate_image(
                prompt=f"anime style, {scene_data['description']}",
                character_ref_url=char_ref_url,
                ar="16:9"
            )
            
            # 3.2 生成配音
            await redis_client.update_task_status(task_id, TaskStatus.GENERATING_AUDIO.value)
            audio_url = await voice_generator.generate_voice(
                text=scene_data["narration"],
                voice="zhiyan"
            )
            
            # 3.3 构建 Scene 对象
            scene = Scene(
                scene_id=scene_id,
                scene_index=idx,
                description=scene_data["description"],
                narration=scene_data["narration"],
                characters=[characters_map[c["name"]] for c in scene_data["characters"]],
                image_url=scene_image_url,
                audio_url=audio_url,
                duration=5.0
            )
            scenes.append(scene)
        
        # === 步骤4: 提交视频服务 ===
        await redis_client.update_task_status(task_id, TaskStatus.SYNTHESIZING_VIDEO.value)
        
        job_id = await video_client.submit_video_synthesis_job(
            task_id=task_id,
            scenes=scenes
        )
        
        # 保存完整任务数据
        task_data = await redis_client.get_task(task_id)
        task_data["scenes"] = [s.model_dump() for s in scenes]
        task_data["video_job_id"] = job_id
        await redis_client.save_task(task_id, task_data)
        
    except Exception as e:
        await redis_client.update_task_status(
            task_id,
            TaskStatus.FAILED.value,
            error=str(e)
        )
        raise
```

---

## 六、相关文档索引

### 代码文件

- **Task模型**: `shared/models/task.py`
- **Scene模型**: `shared/models/scene.py`
- **Character模型**: `shared/models/scene.py`
- **TaskStatus枚举**: `shared/enums.py`
- **重试工具**: `backend/ai-service/app/utils/retry.py`

### 设计文档

- **系统架构**: `docs/ARCHITECTURE.md`
- **API接口**: `docs/API.md`
- **开发规范**: `CLAUDE.md`

### 外部服务文档

- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **Midjourney API**: https://docs.midjourney.com/
- **阿里云 TTS**: https://help.aliyun.com/document_detail/84435.html
- **阿里云 OSS**: https://help.aliyun.com/product/31815.html

---

## 七、更新日志

### v1.0 (2024-10-25)

- 初始版本
- 定义了 6 个直接调用的服务模块
- 添加了完整的输入输出接口文档
- 提供了实现示例代码

---

**维护者**: TFBoys Team  
**最后更新**: 2024-10-25
