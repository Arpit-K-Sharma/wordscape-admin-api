from pydantic import BaseModel, Field
from datetime import date
from bson import ObjectId
from typing import Optional

class IssuedItem(BaseModel):
    order_id: str
    approved_by : str
    issued_date: str


