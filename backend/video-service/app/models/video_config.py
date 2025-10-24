from pydantic import BaseModel
from typing import Optional


class SubtitleStyle(BaseModel):
    font_size: int = 32
    color: str = "white"
    position: str = "bottom"
    font_family: Optional[str] = None
    border_width: int = 2
    border_color: str = "black"


class VideoConfig(BaseModel):
    resolution: str = "1920x1080"
    fps: int = 30
    transition_effect: str = "fade"
    subtitle_style: SubtitleStyle = SubtitleStyle()
