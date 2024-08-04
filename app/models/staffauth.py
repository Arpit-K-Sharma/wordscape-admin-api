from pydantic import BaseModel
from typing import Optional

class StaffAuth(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
