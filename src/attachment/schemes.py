from typing import Literal
from src.schemas import CustomBase

class AttachResponse(CustomBase):
    id: int
    user_filename: str
    system_filename: str
    attach_type: Literal["Icon", "Attach"]