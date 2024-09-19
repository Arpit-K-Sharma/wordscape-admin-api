# app/dto/paper_dto.py
from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class PaperDTO(BaseModel):
    paperType: Optional[str] = None
    rate: Optional[float] = None
    minThickness: Optional[int] = None
    maxThickness: Optional[int] = None

class PaperResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    paperType: str
    rate: float
    minThickness: int
    maxThickness: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("id", pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v