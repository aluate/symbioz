"""
Audiobook data models
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class Book(BaseModel):
    """Book metadata"""
    slug: str
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Role(BaseModel):
    """Voice role configuration"""
    name: str  # e.g., "NARRATOR", "DAD", "BAD_GUY"
    voice_model_id: Optional[str] = None
    default_tone: Optional[str] = None
    default_pacing: Optional[str] = None
    description: Optional[str] = None


class AudioControl(BaseModel):
    """Audio control configuration for a book"""
    roles: Dict[str, Role] = {}
    modifiers: Dict[str, Dict[str, Any]] = {}
    defaults: Dict[str, Any] = {}


class ScriptSegment(BaseModel):
    """A segment of tagged script"""
    role: str
    modifiers: List[str] = []
    text: str
    line_number: Optional[int] = None


class Chapter(BaseModel):
    """Chapter information"""
    id: str
    title: Optional[str] = None
    segments: List[ScriptSegment] = []


class RenderRequest(BaseModel):
    """Request to render audio"""
    book_slug: str
    chapter_id: str
    force_rerender: bool = False


class RenderStatus(BaseModel):
    """Status of an audio render"""
    book_slug: str
    chapter_id: str
    status: str  # "pending", "rendering", "done", "failed"
    file_path: Optional[str] = None
    duration: Optional[float] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None

