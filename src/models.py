from pydantic import BaseModel, ConfigDict

class CustomBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

