from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional

class Department(BaseModel):
    department_name : str
    description : str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        

