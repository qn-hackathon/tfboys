"""
共享枚举类型
"""
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    GENERATING_IMAGES = "generating_images"
    GENERATING_AUDIO = "generating_audio"
    SYNTHESIZING_VIDEO = "synthesizing_video"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoQuality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TTSVoice(str, Enum):
    MALE = "male"
    FEMALE = "female"
    CHILD = "child"
