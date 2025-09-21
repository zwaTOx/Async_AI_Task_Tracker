from src.database import Base, int_pk
from sqlalchemy.orm import Mapped

class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str]
    hashed_password: Mapped[str]