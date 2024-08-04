from pydantic import BaseModel, Field,field_validator, validator
from bson import ObjectId,DBRef
from datetime import datetime

class Leave(BaseModel):
    staff_id: DBRef
    start_date: datetime
    end_date: datetime
    reason: str
    type: str
    filled_on: datetime = Field(default_factory=datetime.now)
    filled_by: str = Field(default="system")
    status: str = "Pending"

    @field_validator("staff_id", mode="before")
    def convert_str_to_dbref(cls, v):
        if isinstance(v, str):
            return DBRef(collection="staff", id=ObjectId(v))
        return v

    @validator("start_date", "end_date", "filled_on", pre=True, always=True)
    def remove_time_from_date(cls, v):
        if isinstance(v, datetime):
            return v.replace(hour=0, minute=0, second=0, microsecond=0)
        return v

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
