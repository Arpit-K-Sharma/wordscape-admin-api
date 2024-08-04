from pydantic import BaseModel, Field, field_validator, validator
from bson import ObjectId
from typing import Optional

class DepartmentDTO(BaseModel):
    id : Optional[str] = Field(default = None, alias="_id")
    department_name : str
    description : str

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
            }
        
    @field_validator('id',mode='before')
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
