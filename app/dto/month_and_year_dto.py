from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Month(BaseModel):
    month: int
    year: Optional[int] = datetime.now().year

    class Config:
        validate_assignment = True

    @property
    def validate_month(self):
        if self.month < 1 or self.month > 12:
            raise ValueError("Month must be between 1 and 12")