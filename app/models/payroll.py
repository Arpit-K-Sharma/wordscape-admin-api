from pydantic import BaseModel, Field, field_validator
from bson import DBRef, ObjectId
from pydantic.json import ENCODERS_BY_TYPE
ENCODERS_BY_TYPE[ObjectId] = str
   

class PyObjectId(ObjectId):
    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def modify_schema(cls, field_schema):
        field_schema.update(type="string")


class PayrollModel(BaseModel):
    id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    month: str
    year: str
    staff_id: DBRef
    working_days: int
    paid_leaves: int
    holidays: int
    weekends: int
    daily_wage: float
    sub_total: float
    tax: float
    net_salary: float

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @field_validator("staff_id", mode="before")
    def convert_str_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection="staff", id=ObjectId(v))
        return v
    

