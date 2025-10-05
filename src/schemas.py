from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CustomBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class TimeStampSchema(CustomBase):
    """Pydantic схема с временными метками."""
    created_at: datetime
    updated_at: datetime