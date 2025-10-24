# Shared - 共享代码模块

包含前后端共享的常量、枚举和异常定义。

## 文件说明

- `constants.py` - 常量定义(任务状态、OSS路径等)
- `enums.py` - 枚举类型(TaskStatus, VideoQuality等)
- `exceptions.py` - 自定义异常类

## 使用示例

```python
from shared.constants import TASK_STATUS_PENDING
from shared.enums import TaskStatus
from shared.exceptions import TaskNotFoundException
```
