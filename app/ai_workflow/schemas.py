from pydantic import BaseModel, Field
from typing import List

class MotivationalContent(BaseModel):
    quotes: List[str] = Field(..., description="Exactly 4 short motivational sentences (4-6 words) following a logical progression.")
    video_title: str = Field(..., description="Short, catchy, SEO-friendly YouTube title")
    youtube_description: str = Field(..., description="SEO-optimized YouTube description with keywords and hashtags")
    video_tags: List[str] = Field(..., description="7-12 relevant YouTube tags")
