# app/dto/plate_dto.py
from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class PlateDTO(BaseModel):
    plateSize: Optional[str] = None
    plateLength: Optional[int] = None
    plateBreadth: Optional[int] = None
    plateRate: Optional[float] = None
    reprint: Optional[float] = None
    inkRate: Optional[float] = None

class PlateResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    plateSize: str
    plateLength: int
    plateBreadth: int
    plateRate: float
    reprint: float
    inkRate: float

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("id", pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v