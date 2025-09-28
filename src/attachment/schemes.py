from typing import Literal
from src.models import CustomBase

class AttachResponse(CustomBase):
    user_filename: str
    system_filename: str
    attach_type: Literal["Icon", "Attach"]