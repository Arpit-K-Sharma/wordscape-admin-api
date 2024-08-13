from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Ink(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    itemName: str
    rate: float
    availability: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}