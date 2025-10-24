"""
场景相关 Schema
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class CharacterResponse(BaseModel):
    """角色响应"""
    character_id: str = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    description: str = Field(..., description="角色描述")
    reference_image_url: Optional[str] = Field(None, description="角色设定图 URL")


class SceneResponse(BaseModel):
    """场景响应"""
    scene_id: str = Field(..., description="场景ID")
    scene_index: int = Field(..., description="场景索引")
    description: str = Field(..., description="场景描述")
    narration: str = Field(..., description="旁白")
    characters: List[CharacterResponse] = Field(default_factory=list, description="角色列表")
    image_url: Optional[str] = Field(None, description="场景图像 URL")
    audio_url: Optional[str] = Field(None, description="配音 URL")
    duration: Optional[float] = Field(None, description="时长")
