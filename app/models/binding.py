# app/models/binding.py
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Binding(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    bindingType: str
    rate: float

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
