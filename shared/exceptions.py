"""
自定义异常
"""


class TFBoysException(Exception):
    """基础异常类"""
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class TaskNotFoundException(TFBoysException):
    """任务未找到"""
    def __init__(self, task_id: str):
        super().__init__(
            message=f"Task {task_id} not found",
            code="TASK_NOT_FOUND"
        )


class APICallException(TFBoysException):
    """API调用失败"""
    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"{service} API call failed: {message}",
            code="API_CALL_FAILED"
        )


class VideoSynthesisException(TFBoysException):
    """视频合成失败"""
    def __init__(self, message: str):
        super().__init__(
            message=f"Video synthesis failed: {message}",
            code="VIDEO_SYNTHESIS_FAILED"
        )
