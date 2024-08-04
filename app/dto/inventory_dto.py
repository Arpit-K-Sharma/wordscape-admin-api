from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional, List

class ItemDTO(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    itemName: str
    availability: int

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class InventoryDTO(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    type: str
    item: List[ItemDTO]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v