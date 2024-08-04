# dtos/purchase_entry_dtos.py
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class ItemDTO(BaseModel):
    code: str 
    itemId : str
    inventoryId : str
    productName: str
    quantity: int
    rate: float
    amount: float

class PurchaseEntryDTO(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    purchaseEntryId : str
    items: List[ItemDTO]
    image: str  
    discount: float
    vat: float
    grandTotal: float
    invoiceNo: str
    invoiceDate: str

    class Config:
        populate_by_name = True
