from pydantic import BaseModel, Field, validator
from typing import List, Optional
from bson import ObjectId, DBRef

class ItemDTO(BaseModel):
    inventoryId : str
    itemId: str
    quantityFromVendor: int
    quantityFromStock: int
    itemCode: Optional[str] = None
    rate: Optional[float] = None
    amount: Optional[float] = None

    @validator('itemId', 'inventoryId', pre=True, always=True)
    def convert_dbref_to_str(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

class PurchaseEntryDTO(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    vendorId: str
    isCompleted: bool
    items: List[ItemDTO]
    tag: Optional[str] = Field(default=None)
    remarks: Optional[str] = Field(default=None)
    image: Optional[str] = None
    discount: Optional[float] = None
    vat: Optional[float] = None
    grandTotal: Optional[float] = None
    invoiceNo: Optional[str] = None
    invoiceDate: Optional[str] = None
    is_issued : Optional[bool] = None

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('vendorId', pre=True, always=True)
    def convert_dbref_to_str(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

class PurchaseOrderDTO(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    orderId: str
    isCompleted: bool
    purchaseEntry: List[PurchaseEntryDTO]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('orderId', pre=True, always=True)
    def convert_dbref_to_str(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

