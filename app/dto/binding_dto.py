from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class BindingDTO(BaseModel):
    bindingType: Optional[str] = None
    rate: Optional[float] = None

class BindingResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    bindingType: str
    rate: float


    class Config:
        populate_by_name= True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("id", pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v