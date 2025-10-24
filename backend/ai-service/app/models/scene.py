from pydantic import BaseModel
from typing import List, Optional


class Character(BaseModel):
    character_id: str
    name: str
    description: str
    reference_image_url: Optional[str] = None


class Scene(BaseModel):
    scene_id: str
    scene_index: int
    description: str
    narration: str
    characters: List[Character]
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    duration: Optional[float] = None
