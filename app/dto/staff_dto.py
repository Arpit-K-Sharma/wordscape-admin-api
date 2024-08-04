from pydantic import BaseModel, Field, validator
from bson import ObjectId,DBRef
from typing import Optional,List
from datetime import datetime

#REQUEST DTO
class StaffDTO(BaseModel):
    fullName : str
    password : Optional[str] = Field(default = None)
    email : str
    address : str
    phoneNumber : str
    status : bool
    role : str = Field(default = "ROLE_USER")
    position : str
    dailyWage : float
    dept_ids: Optional[List[str]] = Field(default=None)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
    
#RESPONSE DTO 
class StaffResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    fullName: str
    email: str
    address: str
    phoneNumber: str
    created_at: Optional[str] = Field(default=None)
    status: bool
    role: str = Field(default="ROLE_USER")
    position: str
    dailyWage: float
    dept_ids: Optional[List[str]] = Field(default=None)
    departmentNames: Optional[List[str]] = Field(default=None)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }

    @validator('id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('dept_ids', pre=True, always=True)
    def convert_dbrefs_to_strs(cls, v):
        if isinstance(v, list):
            return [str(dbref.id) if isinstance(dbref, DBRef) else dbref for dbref in v]
        return v

    @validator('created_at', pre=True, always=True)
    def convert_datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.strftime("%d-%m-%Y")
        return v

