"""
场景和角色数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Character(BaseModel):
    """角色模型"""
    character_id: str = Field(..., description="角色唯一标识")
    name: str = Field(..., description="角色名称")
    description: str = Field(..., description="角色外貌描述(用于图像生成)")
    reference_image_url: Optional[str] = Field(None, description="角色设定图 URL")
    midjourney_cref_url: Optional[str] = Field(None, description="Midjourney --cref 参数 URL")
    first_appearance_scene: Optional[int] = Field(None, description="首次出现的场景索引")
    created_at: Optional[datetime] = Field(None, description="创建时间")


class Scene(BaseModel):
    """场景模型"""
    scene_id: str = Field(..., description="场景唯一标识")
    scene_index: int = Field(..., description="场景索引(从0开始)")
    description: str = Field(..., description="场景描述(用于图像生成)")
    narration: str = Field(..., description="旁白文字(用于配音)")
    characters: List[Character] = Field(default_factory=list, description="场景中的角色列表")
    image_url: Optional[str] = Field(None, description="生成的场景图像 URL")
    audio_url: Optional[str] = Field(None, description="生成的配音 URL")
    duration: Optional[float] = Field(None, description="音频时长(秒)")
