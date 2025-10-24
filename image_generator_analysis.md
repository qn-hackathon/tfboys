# image_generator 实现逻辑分析

根据项目文档和代码结构分析,以下是 `backend/ai-service/app/services/image_generator.py` 的完整实现方案。

---

## 一、功能需求分析

### 核心功能
`ImageGenerator` 服务负责使用 **Midjourney API** 生成动漫风格图像,是整个视频生成流程中的关键环节:

1. **生成角色设定图** - 为每个角色生成初始参考图像
2. **生成场景图像** - 根据场景描述生成带有角色的场景图
3. **保持角色一致性** - 使用 Midjourney 的 `--cref` 参数确保同一角色在不同场景中外观一致

### 数据流程位置
```
文本分析 → 角色提取 → [角色设定图生成] → [场景图像生成] → 配音生成 → 视频合成
                           ↑                    ↑
                      ImageGenerator      ImageGenerator
```

---

## 二、实现逻辑设计

### 2.1 类结构设计

```python
class ImageGenerator:
    """
    图像生成服务 - 使用 Midjourney API 生成动漫风格图像
    
    功能:
    1. generate_character_image() - 生成角色设定图(无 --cref)
    2. generate_scene_image() - 生成场景图像(使用 --cref)
    3. _build_prompt() - 构建 Midjourney 提示词
    4. _submit_task() - 提交生成任务到 Midjourney API
    5. _wait_for_result() - 轮询任务结果
    6. _upload_to_oss() - 上传图像到阿里云 OSS
    """
```

### 2.2 核心方法实现逻辑

#### 方法 1: `generate_character_image(character: Character) -> str`

**功能**: 生成角色设定图(Character Design Sheet)

**实现步骤**:
1. 根据 `Character.description` 构建提示词
2. 添加固定参数: `--ar 1:1 --niji 6` (方形比例,动漫模型)
3. 提交到 Midjourney API
4. 轮询等待生成结果(通常 30-60 秒)
5. 下载图像并上传到 OSS (`characters/{character_id}.jpg`)
6. 返回 OSS 公开访问 URL

**提示词模板**:
```
anime style, character design sheet, {character_name}, {description}, white background --ar 1:1 --niji 6
```

**示例**:
```python
# 输入: Character(name="小明", description="short black hair, blue eyes, wearing school uniform")
# 输出提示词: "anime style, character design sheet, 小明, short black hair, blue eyes, wearing school uniform, white background --ar 1:1 --niji 6"
# 返回: "https://tfboys.oss-cn-hangzhou.aliyuncs.com/characters/char_001.jpg"
```

---

#### 方法 2: `generate_scene_image(scene: Scene, characters: List[Character]) -> str`

**功能**: 生成场景图像(使用角色参考图保持一致性)

**实现步骤**:
1. 根据 `Scene.description` 构建基础提示词
2. 添加场景中出现的角色名称和动作
3. 收集角色的 `reference_image_url` 用于 `--cref` 参数
4. 添加参数: `--ar 16:9 --niji 6 --cref <url1> <url2> --cw 100`
5. 提交到 Midjourney API
6. 轮询等待生成结果
7. 下载图像并上传到 OSS (`scenes/{task_id}/{scene_id}.jpg`)
8. 返回 OSS 公开访问 URL

**提示词模板**:
```
anime style, {scene_description}, {character1_name} {action1}, {character2_name} {action2} --ar 16:9 --niji 6 --cref {ref_url1} {ref_url2} --cw 100
```

**`--cref` 参数说明**:
- `--cref <url1> <url2> ...`: 可以传入多个角色参考图 URL(空格分隔)
- `--cw 100`: Character Weight (权重 0-100),100 表示严格遵循参考图外观

**示例**:
```python
# 输入: Scene(description="park with cherry blossoms, sunny day")
#       Characters: [小明, 小红]
# 输出提示词: "anime style, park with cherry blossoms, sunny day, 小明 standing, 小红 sitting on bench --ar 16:9 --niji 6 --cref https://oss.../char_001.jpg https://oss.../char_002.jpg --cw 100"
# 返回: "https://tfboys.oss-cn-hangzhou.aliyuncs.com/scenes/task_123/scene_001.jpg"
```

---

#### 方法 3: `_submit_task(prompt: str) -> str`

**功能**: 提交任务到 Midjourney API

**实现步骤**:
1. 构建 HTTP 请求:
   ```python
   POST {midjourney_api_url}/imagine
   Headers: {"Authorization": f"Bearer {api_key}"}
   Body: {"prompt": prompt}
   ```
2. 解析响应获取 `task_id`
3. 返回 `task_id` 用于后续轮询

---

#### 方法 4: `_wait_for_result(task_id: str, timeout: int = 300) -> str`

**功能**: 轮询任务结果(最多等待 5 分钟)

**实现步骤**:
1. 每隔 10 秒查询任务状态:
   ```python
   GET {midjourney_api_url}/tasks/{task_id}
   ```
2. 检查状态:
   - `pending` / `processing`: 继续等待
   - `completed`: 返回图像 URL
   - `failed`: 抛出异常
3. 使用 `tenacity` 库实现重试逻辑(已在 requirements.txt 中)

---

#### 方法 5: `_upload_to_oss(image_url: str, oss_path: str) -> str`

**功能**: 下载 Midjourney 图像并上传到阿里云 OSS

**实现步骤**:
1. 使用 `httpx` 下载图像
2. 使用 `shared/clients/oss_client.py` 上传到 OSS
3. 设置为公开读权限
4. 返回 OSS 公开访问 URL

---

## 三、外部依赖

### 3.1 Midjourney API

**重要说明**: Midjourney **官方不提供公开 API**,需要使用第三方代理服务。

#### 推荐方案 1: **GoAPI** (推荐)
- **官网**: https://www.goapi.ai
- **文档**: https://docs.goapi.ai/api-reference/midjourney
- **定价**: $0.03-0.12 / 图(根据模型和分辨率)
- **特点**: 
  - 支持 `--cref` 参数 ✅
  - 支持 Niji 6 动漫模型 ✅
  - 响应速度快(30-60 秒)
  - 提供 REST API 和 WebSocket

**API 端点**:
```
POST https://api.goapi.ai/mj/v2/imagine
GET  https://api.goapi.ai/mj/v2/fetch/{task_id}
```

**请求示例**:
```python
import httpx

async def submit_midjourney_task(prompt: str, api_key: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.goapi.ai/mj/v2/imagine",
            headers={"X-API-Key": api_key},
            json={
                "prompt": prompt,
                "process_mode": "fast"  # fast/relax/turbo
            }
        )
        data = response.json()
        return data["task_id"]

async def fetch_result(task_id: str, api_key: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.goapi.ai/mj/v2/fetch/{task_id}",
            headers={"X-API-Key": api_key}
        )
        return response.json()
```

---

#### 推荐方案 2: **UseAPI**
- **官网**: https://www.useapi.net
- **文档**: https://docs.useapi.net/api-reference/midjourney-api
- **定价**: $0.05 / 图
- **特点**: 支持 `--cref`,中文友好

---

#### 推荐方案 3: **自建代理** (Discord Bot)
- 使用开源项目: https://github.com/erictik/midjourney-api
- 需要自己的 Discord 账号和 Midjourney 订阅
- 成本: Midjourney 订阅费用($10-60/月)

---

### 3.2 阿里云 OSS

**用途**: 存储生成的图像

**依赖**:
- `oss2==2.18.4` (已在 requirements.txt 中)
- 配置项: `OSS_ENDPOINT`, `OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET`, `OSS_BUCKET_NAME`

**集成方式**: 使用 `shared/clients/oss_client.py`

---

### 3.3 其他依赖

| 依赖 | 用途 | 状态 |
|------|------|------|
| `httpx==0.25.2` | HTTP 客户端(调用 Midjourney API) | ✅ 已安装 |
| `tenacity==8.2.3` | 重试机制 | ✅ 已安装 |
| `pillow==10.1.0` | 图像处理(可选,用于压缩/裁剪) | ✅ 已安装 |
| `aiofiles==23.2.1` | 异步文件操作 | ✅ 已安装 |

---

## 四、配置项

需要在 `backend/ai-service/.env` 中添加:

```env
# Midjourney API (使用 GoAPI 为例)
MIDJOURNEY_API_KEY=goapi_xxxxxxxxxxxxxxxx
MIDJOURNEY_API_URL=https://api.goapi.ai/mj/v2

# 阿里云 OSS (已存在)
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_ACCESS_KEY_ID=LTAI5...
OSS_ACCESS_KEY_SECRET=xxx
OSS_BUCKET_NAME=tfboys
```

---

## 五、异常处理

### 需要处理的异常

1. **API 调用失败** (网络错误、超时)
   - 使用 `tenacity` 重试 3 次
   - 重试间隔: 2 秒 * 2^n(指数退避)

2. **任务超时** (5 分钟内未完成)
   - 抛出 `ImageGenerationException`
   - 记录日志并通知上层

3. **图像生成失败** (Midjourney 返回 failed 状态)
   - 检查错误原因(提示词违规、余额不足等)
   - 抛出详细异常信息

4. **OSS 上传失败**
   - 重试 3 次
   - 失败后保留 Midjourney 原始 URL

### 自定义异常类

```python
class ImageGenerationException(Exception):
    """图像生成异常"""
    pass
```

---

## 六、性能优化建议

### 6.1 并发生成
- 使用 `asyncio.gather()` 并发生成多个场景图像
- 限制并发数量(建议 3-5 个,避免超过 API 速率限制)

### 6.2 缓存机制
- 如果相同角色的设定图已生成,直接从 Redis 获取 URL
- Key 格式: `character:{task_id}:{character_name}:ref_image`

### 6.3 轮询优化
- 使用指数退避策略: 5s → 10s → 15s → 20s
- 前 30 秒每 5 秒轮询一次,之后每 15 秒轮询一次

---

## 七、测试策略

### 单元测试
```python
@pytest.mark.asyncio
async def test_generate_character_image():
    generator = ImageGenerator()
    character = Character(
        character_id="char_001",
        name="小明",
        description="short black hair, blue eyes"
    )
    
    # Mock Midjourney API
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value.json.return_value = {"task_id": "task_123"}
        
        url = await generator.generate_character_image(character)
        
        assert url.startswith("https://tfboys.oss")
```

### 集成测试
- 使用真实 Midjourney API(测试环境)
- 验证生成的图像 URL 可访问
- 检查 OSS 文件是否正确上传

---

## 八、实现优先级

### Phase 1: 基础功能 (MVP)
- [x] 提示词构建逻辑
- [ ] Midjourney API 集成(`_submit_task`, `_wait_for_result`)
- [ ] OSS 上传功能
- [ ] 基础异常处理

### Phase 2: 角色一致性
- [ ] `--cref` 参数支持
- [ ] 角色参考图管理
- [ ] 多角色场景生成

### Phase 3: 优化
- [ ] 并发生成优化
- [ ] 缓存机制
- [ ] 错误重试优化
- [ ] 日志和监控

---

## 九、成本估算

### Midjourney API 成本(使用 GoAPI)

| 项目 | 数量 | 单价 | 小计 |
|------|------|------|------|
| 角色设定图 | 5 个角色 | $0.05 | $0.25 |
| 场景图像 | 20 个场景 | $0.08 | $1.60 |
| **总计** | - | - | **$1.85 / 任务** |

### 阿里云 OSS 成本
- 存储: ~$0.02 / GB / 月(可忽略不计)
- 流量: ~$0.12 / GB(公网下行)

---

## 十、推荐的实现顺序

1. **第一步**: 选择 Midjourney API 代理服务(推荐 GoAPI)
2. **第二步**: 实现 `_submit_task()` 和 `_wait_for_result()`
3. **第三步**: 实现 `generate_character_image()` (不带 --cref)
4. **第四步**: 测试角色设定图生成流程
5. **第五步**: 实现 `generate_scene_image()` (带 --cref)
6. **第六步**: 集成到 `app/workers/tasks.py` 工作流
7. **第七步**: 性能优化和异常处理完善

---

## 相关文件

- 数据模型: `/workspace/shared/models/scene.py`
- 角色管理: `/workspace/backend/ai-service/app/services/character_manager.py`
- 配置管理: `/workspace/backend/ai-service/app/config.py`
- 工作流: `/workspace/backend/ai-service/app/workers/tasks.py`

---

## 总结

`ImageGenerator` 服务的核心是:
1. **封装 Midjourney API 调用逻辑** (提交任务 → 轮询结果)
2. **实现角色一致性** (使用 `--cref` 参数引用角色设定图)
3. **集成 OSS 存储** (保存生成的图像)

**关键技术点**:
- Midjourney 的 `--cref` + `--cw 100` 确保角色外观一致
- 异步轮询 + 重试机制确保生成成功
- OSS 公开读权限确保图像可直接访问

**外部依赖**:
- Midjourney API 代理服务(推荐 GoAPI: https://www.goapi.ai)
- 阿里云 OSS 对象存储

如有任何疑问或需要进一步讨论的地方,请随时提出!
