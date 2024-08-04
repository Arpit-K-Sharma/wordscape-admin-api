from pydantic import BaseModel, Field, validator
from bson import ObjectId, DBRef
from typing import List, Optional

class Items(BaseModel):
    itemId: DBRef
    inventoryId: DBRef
    code: str
    productName: str
    quantity: int
    rate: float
    amount: float

    @validator('itemId', pre=True, always=True)
    def convert_item_id_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection='inventory', id=v)
        return v
    
    @validator('inventoryId', pre=True, always=True)
    def convert_inventory_id_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection='inventory', id=v)
        return v

    class Config:
        arbitrary_types_allowed = True

class PurchaseEntry(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    purchaseEntryId: DBRef
    items: List[Items]
    image: str
    discount: float
    vat: float
    grandTotal: float
    invoiceNo: str
    invoiceDate: str

    @validator('purchaseEntryId', pre=True, always=True)
    def convert_purchase_entry_id_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection='purchase_entries', id=v)
        return v

    class Config:
        arbitrary_types_allowed = True
