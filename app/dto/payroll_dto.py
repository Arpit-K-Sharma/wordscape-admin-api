from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional

class PayrollDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    staff_id: str
    staff_name:str
    month: str
    year: str
    working_days: int
    paid_leaves: int
    holidays: int
    weekends: Optional[int]
    daily_wage: float
    sub_total: Optional[float] = None
    tax: Optional[float] = None
    net_salary: Optional[float] = None

    @validator("id", pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
