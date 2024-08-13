# app/dto/customer_dto.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from bson import ObjectId

class CustomerDTO(BaseModel):
    fullName: str
    email: str
    phoneNumber: str
    address: Optional[str] = None
    companyName: Optional[str] = None
    status: bool = True

class CustomerResponseDTO(BaseModel):
    id: str = Field(default=None, alias="_id")
    fullName: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    phoneNumber: Optional[str] = None
    companyName: Optional[str] = None
    status: Optional[bool] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @validator('id', pre=True)
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
class CustomerListResponseDTO(BaseModel):
    customers: List[CustomerResponseDTO]
    total_elements: int