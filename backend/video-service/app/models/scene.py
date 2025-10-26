from pydantic import BaseModel, Field
from typing import Optional


class Scene(BaseModel):
    """场景模型"""
    scene_id: str = Field(..., description="场景唯一标识")
    scene_index: int = Field(..., description="场景索引(从0开始)")
    description: str = Field(..., description="场景描述(用于图像生成)")
    narration: str = Field(..., description="旁白文字(用于配音)")
    subtitle_text: Optional[str] = Field(None, description="字幕文本")
    image_url: Optional[str] = Field(None, description="生成的场景图像 URL")
    audio_url: Optional[str] = Field(None, description="生成的配音 URL")
    duration: Optional[float] = Field(None, description="音频时长(秒)")
