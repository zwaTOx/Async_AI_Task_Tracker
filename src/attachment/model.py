from typing import Literal, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table
from src.database import Base, int_pk

AttachmentType = Literal["Icon", "Attach"]

attachment_task = Table(
    "attachment_task",
    Base.metadata,
    Column("attachment_id", Integer, ForeignKey("attachments.id", ondelete="CASCADE"), primary_key=True),
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
)

class Attachment(Base):
    id: Mapped[int_pk]
    user_filename: Mapped[str]
    system_filename: Mapped[str]
    attach_type: Mapped[AttachmentType] = mapped_column(default="Icon")

    tasks = relationship("Task", secondary=attachment_task, back_populates="attachments")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))