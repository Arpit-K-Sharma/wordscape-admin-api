from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId, DBRef

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ItemModel(BaseModel):
    inventory_id: DBRef
    item_id: DBRef
    quantity: int
    reason: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, DBRef: lambda x: str(x.id)}

class LeftoverModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    order_id: DBRef
    items: List[ItemModel]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, DBRef: lambda x: str(x.id)}