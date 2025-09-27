from datetime import datetime
from src.models import CustomBase


class CodeResponse(CustomBase):
    code: str
    code_type: str
    is_used: bool
    created_at: datetime
    user_id: int