
from pydantic import BaseModel
from typing import List

class ItemDTO(BaseModel):
    item_id: str
    quantity: int
    inventory_id: str
    reason: str

class LeftoverDTO(BaseModel):
    order_id: str
    items: List[ItemDTO]

class UpdateItemDTO(BaseModel):
    item_id: str
    inventory_id: str
    quantity: int
    reason: str