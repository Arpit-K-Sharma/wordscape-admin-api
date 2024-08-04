from pydantic import BaseModel

class AdminAuth(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


    