from sqlalchemy import Enum

class Role(str, Enum):
    OWNER = "OWNER"                 
    ADMINISTRATOR = "ADMINISTRATOR" 
    READER = "READER"               
    USER = "USER"                   
    INVITED = "INVITED"             # приглашенный в проект