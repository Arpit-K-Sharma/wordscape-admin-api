from pydantic import BaseModel, Field, validator
from bson import ObjectId,DBRef
from typing import Optional,List
from datetime import datetime

class Staff(BaseModel):
    fullName : str
    password : Optional[str] = Field(default = None)
    email : str
    address : str
    phoneNumber : str
    created_at : Optional[datetime] = Field(default = None)
    status : bool
    role : str = Field(default = "ROLE_USER")
    position : str
    dailyWage : float
    dept_ids: List[DBRef]
    departmentNames: Optional[List[str]] = Field(default=None)

    @validator('dept_ids', pre=True, always=True)
    def convert_strings_to_dbrefs(cls, v):
        if isinstance(v, list):
            return [DBRef(collection='department', id=ObjectId(dept_id)) if isinstance(dept_id, str) else dept_id for dept_id in v]
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            DBRef: lambda dbref: str(dbref.id)
        }


