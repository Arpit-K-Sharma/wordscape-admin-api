from pydantic import BaseModel, Field, validator, model_validator
from bson import ObjectId,DBRef
from typing import Optional,List
from datetime import datetime

#REQUEST DTO
class LeaveDTO(BaseModel):
    id : Optional[str] = Field(default = None, alias="_id")
    staff_id: Optional[str] = Field(default = None)
    start_date: datetime
    end_date: datetime
    reason: str
    type: str
    filled_on : Optional[datetime] = Field(default = datetime.now)
    filled_by : Optional[str] = Field(default = "system")
    status: str = Field(default = "Pending")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


#RESPONSE DTO
class LeaveResponseDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    staff_id: Optional[str] = Field(default=None)   
    staff_name: Optional[str] = Field(default=None)
    start_date: str
    end_date: str
    reason: str
    type: str
    filled_on: Optional[str] = Field(default=None)
    filled_by: Optional[str] = Field(default=None)
    status: str = Field(default="Pending")

    @validator("id", pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("staff_id", pre=True, always=True)
    def convert_dbref_to_str(cls, v):
        if isinstance(v, DBRef):
            return str(v.id)
        return v

    @model_validator(mode='before')
    def convert_datetime_to_str(cls, values):
        for field in ['start_date', 'end_date', 'filled_on']:
            if isinstance(values.get(field), datetime):
                values[field] = values[field].strftime("%d-%m-%Y")  # Convert to DD-MM-YYYY format
        return values

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

