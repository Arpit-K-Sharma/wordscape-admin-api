# app/dto/paper_thickness_dto.py
from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class PaperThicknessDTO(BaseModel):
    thickness: int

class PaperThicknessResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    thickness: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("id", pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v