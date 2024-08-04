from pydantic import BaseModel, Field, validator
from typing import List, Optional
from bson import ObjectId, DBRef

class Item(BaseModel):
    inventoryId : DBRef
    itemId: DBRef
    quantityFromVendor: int
    quantityFromStock: int
    itemCode: Optional[str] = None
    rate: Optional[float] = None
    amount: Optional[float] = None

    @validator('itemId', pre=True, always=True)
    def convert_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection="inventory", id=v)
        return v

    class Config:
        arbitrary_types_allowed = True

    @validator('inventoryId', pre=True, always=True)
    def convert_inventory_id_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection="inventory", id=v)
        return v
    
    class Config:
        arbitrary_types_allowed = True

class PurchaseEntry(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    vendorId: DBRef
    isCompleted: bool
    tag: Optional[str] = Field(default=None)
    remarks: Optional[str] = Field(default=None)
    items: List[Item]
    image: Optional[str] = None
    discount: Optional[float] = None
    vat: Optional[float] = None
    grandTotal: Optional[float] = None
    invoiceNo: Optional[str] = None
    invoiceDate: Optional[str] = None

    @validator('vendorId', pre=True, always=True)
    def convert_vendor_id_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection="vendors", id=v)
        return v

    class Config:
        arbitrary_types_allowed = True

class PurchaseOrder(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    orderId: DBRef
    isCompleted: bool
    purchaseEntry: List[PurchaseEntry]

    @validator('orderId', pre=True, always=True)
    def convert_order_id_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection="orders", id=v)
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


