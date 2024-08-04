from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List

class Items(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    itemName: str
    availability: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class InventoryItem(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    type: str
    item: List[Items]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}