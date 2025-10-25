# AI Service 测试文档

## 📋 概述

本测试套件为 AI Service 提供全面的单元测试和集成测试,确保代码质量和功能正确性。

## 🏗️ 测试结构

```
tests/
├── conftest.py              # pytest配置和共享fixtures
├── unit/                    # 单元测试(快速,隔离)
│   ├── services/            # 服务层测试
│   │   ├── test_text_analyzer.py
│   │   ├── test_image_generator.py
│   │   ├── test_character_manager.py
│   │   ├── test_voice_generator.py
│   │   └── test_video_client.py
│   └── utils/               # 工具函数测试
│       └── test_retry.py
└── integration/             # 集成测试(较慢,需要外部服务)
    └── test_workflow.py     # 完整工作流程测试
```

## 🚀 快速开始

### 1. 安装测试依赖

```bash
cd backend/ai-service
pip install -r requirements.txt -r requirements-test.txt
```

### 2. 运行测试

#### 运行所有测试
```bash
python run_tests.py
```

#### 仅运行单元测试
```bash
python run_tests.py --unit
```

#### 仅运行集成测试
```bash
python run_tests.py --integration
```

#### 生成覆盖率报告
```bash
python run_tests.py --cov
```

#### 详细输出
```bash
python run_tests.py -v
```

### 3. 使用 pytest 直接运行

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest -m unit

# 运行集成测试
pytest -m integration

# 生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定测试文件
pytest tests/unit/services/test_text_analyzer.py

# 运行特定测试函数
pytest tests/unit/services/test_text_analyzer.py::TestTextAnalyzer::test_analyze_novel_success
```

## 📝 测试覆盖范围

### 单元测试

#### 服务层 (Services)

1. **TextAnalyzer** (`test_text_analyzer.py`)
   - ✅ 成功分析小说文本
   - ✅ 处理无效JSON响应
   - ✅ API调用失败处理
   - ✅ 不同长度文本的提示词生成
   - ✅ 角色描述归一化

2. **ImageGenerator** (`test_image_generator.py`)
   - ✅ 成功生成角色图像
   - ✅ 成功生成场景图像
   - ✅ 不同宽高比支持
   - ✅ API调用失败处理
   - ✅ 图像下载失败处理

3. **CharacterManager** (`test_character_manager.py`)
   - ✅ 处理新角色
   - ✅ 获取已存在角色
   - ✅ 角色ID生成
   - ✅ 批量获取角色引用
   - ✅ 列出任务角色

4. **VoiceGenerator** (`test_voice_generator.py`)
   - ✅ 成功生成配音
   - ✅ 不同音色支持
   - ✅ 七牛云Token生成
   - ✅ TTS API调用
   - ✅ 音频时长获取

5. **VideoClient** (`test_video_client.py`)
   - ✅ 提交视频合成任务
   - ✅ 获取任务状态
   - ✅ HTTP错误处理
   - ✅ 上下文管理器

#### 工具层 (Utils)

1. **RetryDecorator** (`test_retry.py`)
   - ✅ 首次成功
   - ✅ 重试后成功
   - ✅ 全部失败
   - ✅ 指数退避
   - ✅ 同步版本

### 集成测试

1. **完整工作流程** (`test_workflow.py`)
   - ✅ 端到端成功流程
   - ✅ 文本分析失败
   - ✅ 空场景处理
   - ✅ 视频提交失败

## 🧪 编写测试指南

### 测试命名规范

- 测试文件: `test_<module_name>.py`
- 测试类: `Test<ClassName>`
- 测试函数: `test_<function_name>_<scenario>`

示例:
```python
class TestTextAnalyzer:
    def test_analyze_novel_success(self):
        """测试成功分析小说"""
        pass
    
    def test_analyze_novel_invalid_json(self):
        """测试无效JSON响应"""
        pass
```

### 使用 Fixtures

项目在 `conftest.py` 中提供了常用的 fixtures:

```python
@pytest.mark.unit
class TestMyService:
    def test_with_redis(self, mock_redis_client):
        # mock_redis_client 自动注入
        pass
    
    def test_with_sample_data(self, sample_novel_text, sample_scenes_data):
        # 使用示例数据
        pass
```

### Mock 外部依赖

单元测试应该隔离外部依赖:

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_my_function():
    with patch('app.services.external_api.call', return_value="mocked"):
        result = await my_function()
        assert result == "expected"
```

### 测试异步函数

使用 `@pytest.mark.asyncio` 装饰器:

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### 标记测试类型

使用 pytest markers 区分测试类型:

```python
@pytest.mark.unit
def test_unit():
    pass

@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.slow
def test_slow():
    pass
```

## 📊 覆盖率目标

- **总体覆盖率**: ≥ 80%
- **核心业务逻辑**: ≥ 90%
- **工具函数**: ≥ 85%

## 🐛 调试测试

### 打印调试信息

```bash
pytest -s  # 显示print输出
```

### 只运行失败的测试

```bash
pytest --lf  # last failed
```

### 进入调试器

```python
def test_something():
    import pdb; pdb.set_trace()
    # 代码会在这里暂停
```

或使用 pytest 的断点:

```bash
pytest --pdb  # 失败时自动进入调试器
```

## 🔧 CI/CD 集成

在 CI/CD 管道中运行测试:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: |
          cd backend/ai-service
          pip install -r requirements.txt -r requirements-test.txt
      - name: Run tests
        run: |
          cd backend/ai-service
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 📚 参考资源

- [pytest 文档](https://docs.pytest.org/)
- [pytest-asyncio 文档](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock 文档](https://docs.python.org/3/library/unittest.mock.html)

## ❓ 常见问题

### Q: 测试运行很慢怎么办?

A: 使用 `-n auto` 并行运行测试 (需要安装 pytest-xdist):
```bash
pip install pytest-xdist
pytest -n auto
```

### Q: 如何跳过某些测试?

A: 使用 `@pytest.mark.skip` 或 `@pytest.mark.skipif`:
```python
@pytest.mark.skip(reason="暂时跳过")
def test_something():
    pass
```

### Q: 如何测试异常?

A: 使用 `pytest.raises`:
```python
def test_exception():
    with pytest.raises(ValueError, match="error message"):
        raise ValueError("error message")
```

## 🤝 贡献指南

1. 所有新功能必须有对应的单元测试
2. 修复 bug 时,先写失败的测试,再修复
3. 保持测试覆盖率不低于 80%
4. 测试应该快速、独立、可重复

---

**最后更新**: 2024-10-25
**维护者**: TFBoys Team
