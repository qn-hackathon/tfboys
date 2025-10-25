from pydantic import BaseModel


class Scene(BaseModel):
    scene_id: str
    scene_index: int
    description: str
    narration: str
    image_url: str
    audio_url: str
    audio_duration: float
    subtitle_text: str
