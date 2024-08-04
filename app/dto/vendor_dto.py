from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional

class VendorDTO(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    vendorName: str
    vendorAddress: str
    vendorVAT: str
    vendorPhone: str

    @validator('id', pre=True)
    def validate_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value
