from datetime import datetime
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from bson import ObjectId

#REQUEST DTO
class HolidayDTO(BaseModel):
    holiday_id: Optional[str] = Field(default = None, alias="holiday_id")
    name: str
    date: datetime
    description: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
            }
        
    @validator('holiday_id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class YearlyHolidaysDTO(BaseModel):
    year: int
    holidays: List[HolidayDTO]


#RESPONSE DTO
class HolidayResponseDTO(BaseModel):
    holiday_id: Optional[str] = Field(default = None, alias="holiday_id")
    name: str
    date: str
    description: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
            }
        
    @validator('holiday_id', pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator('date', pre=True, always=True)
    def convert_datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.strftime("%d-%m-%Y")
        return v

class YearlyHolidaysResponseDTO(BaseModel):
    year: int
    holidays: List[HolidayResponseDTO]
