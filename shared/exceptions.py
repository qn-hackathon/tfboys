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


class TextAnalysisException(TFBoysException):
    """文本分析失败"""
    def __init__(self, message: str):
        super().__init__(
            message=f"Text analysis failed: {message}",
            code="TEXT_ANALYSIS_FAILED"
        )


class ImageGenerationException(TFBoysException):
    """图像生成失败"""
    def __init__(self, message: str):
        super().__init__(
            message=f"Image generation failed: {message}",
            code="IMAGE_GENERATION_FAILED"
        )


class VoiceGenerationException(TFBoysException):
    """配音生成失败"""
    def __init__(self, message: str):
        super().__init__(
            message=f"Voice generation failed: {message}",
            code="VOICE_GENERATION_FAILED"
        )


class CharacterManagementException(TFBoysException):
    """角色管理失败"""
    def __init__(self, message: str):
        super().__init__(
            message=f"Character management failed: {message}",
            code="CHARACTER_MANAGEMENT_FAILED"
        )


class OSSException(TFBoysException):
    """OSS操作失败"""
    def __init__(self, message: str):
        super().__init__(
            message=f"OSS operation failed: {message}",
            code="OSS_OPERATION_FAILED"
        )
