from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str = "New project"
    prompt: str = ""
    niche: str = ""
    goal: str = "reach"  # reach | sales | followers | community

class ProjectOut(BaseModel):
    id: int
    created_at: datetime
    title: str
    prompt: str
    niche: str
    goal: str
    status: str
    generation_json: Dict[str, Any]
    render_json: Dict[str, Any]
    publish_json: Dict[str, Any]

    class Config:
        from_attributes = True

class AssetOut(BaseModel):
    id: int
    project_id: int
    created_at: datetime
    kind: str
    filename: str
    content_type: str
    url: str
    class Config:
        from_attributes = True

class GenerationRequest(BaseModel):
    project_id: int
    language: str = "pt"
    tone: str = "direto"
    max_duration_sec: int = 18

class RenderRequest(BaseModel):
    project_id: int
    variant: str = "A"  # A | B
    burn_captions: bool = True

class PublishRequest(BaseModel):
    project_id: int
    caption: Optional[str] = None
    media_url: Optional[str] = None  # if None, uses rendered output (must be public in prod)
    media_type: str = "REELS"  # REELS | IMAGE | VIDEO
