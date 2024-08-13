# app/dto/paper_size_dto.py
from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class PaperSizeDTO(BaseModel):
    paperSize: Optional[str] = None
    dimensions: Optional[str] = None
    paperLength: Optional[float] = None
    paperBreadth: Optional[float] = None

class PaperSizeResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    paperSize: str
    dimensions: str
    paperLength: float
    paperBreadth: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("id", pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v