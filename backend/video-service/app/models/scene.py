from pydantic import BaseModel
from typing import List, Optional


class Character(BaseModel):
    character_id: str
    name: str
    reference_image_url: Optional[str] = None


class Scene(BaseModel):
    scene_id: str
    scene_index: int
    description: str
    narration: str
    characters: List[Character] = []
    image_url: str
    audio_url: str
    audio_duration: float
    subtitle_text: str
