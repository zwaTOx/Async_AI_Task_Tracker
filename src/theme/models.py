from src.database import Base, int_pk
from src.models import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table
from datetime import datetime, timedelta

class Theme(Base, TimeStampMixin):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    max_voices: Mapped[int] = mapped_column(default=1)
    time_start_idea: Mapped[datetime] = mapped_column(default=datetime.now()+timedelta(hours=0))  # in hours
    time_start_vote: Mapped[datetime] = mapped_column(default=datetime.now()+timedelta(hours=24))  # in hours
    time_end_vote: Mapped[datetime] = mapped_column(default=datetime.now()+timedelta(hours=48))   # in hours
    is_archived: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))