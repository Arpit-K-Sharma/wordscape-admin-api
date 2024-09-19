from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class InkDTO(BaseModel):
    inkType: Optional[str] = None

class InkResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    inkType: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("id", pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v