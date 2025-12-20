from typing import Literal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.database import Base, int_pk

AttachmentType = Literal["Icon", "Attach"]

class Attachment(Base):
    id: Mapped[int_pk]
    user_filename: Mapped[str]
    system_filename: Mapped[str]
    attach_type: Mapped[AttachmentType] = mapped_column(default="Icon")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))