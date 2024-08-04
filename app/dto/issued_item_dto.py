# dtos/issued_item_dtos.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class IssuedItemDTO(BaseModel):
    id: Optional[str] = Field(default_factory=str, alias="_id")
    order_id: str
    approved_by : str
    issued_date: str

    class Config:
        populate_by_name = True
