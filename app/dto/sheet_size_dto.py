from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional

class SheetSizeDTO(BaseModel):
    sheetSize: Optional[str] = None
    sheetLength: Optional[int] = None
    sheetBreadth: Optional[int] = None
    value: Optional[int] = None

class SheetSizeResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    sheetSize: str
    sheetLength: int
    sheetBreadth: int
    value: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("id", pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
