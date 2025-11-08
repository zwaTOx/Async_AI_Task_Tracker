from typing import Literal, Optional
from src.schemas import CustomBase
from pydantic import Field

class ThemeBase(CustomBase):
    name: str
    description: Optional[str] = None
    
class ThemeCreate(ThemeBase):
    max_voices: Optional[int] = Field(default=1, ge=1)

class ThemeUpdate(CustomBase):
    name: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[Literal["Brainshtorm", "Vote", "Finish"]] = None
    max_voices: Optional[int] = Field(default=None, ge=1)
