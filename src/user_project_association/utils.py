from typing import Literal
from sqlalchemy import Enum

Roles = Literal["OWNER", "USER", "ADMINISTRATOR", "USER", "READER"]
