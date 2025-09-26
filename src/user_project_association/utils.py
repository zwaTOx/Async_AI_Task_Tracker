from typing import Literal
from sqlalchemy import Enum

Inv_Roles = Literal["USER", "READER"]
Update_Roles = Literal["USER", "READER", "ADMINISTRATOR"]
Roles = Literal["OWNER", "USER", "ADMINISTRATOR", "USER", "READER"]
