from pydantic import BaseModel, Field
from typing import Optional

def to_camel(string: str) -> str:
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

class ProjectTrackingDTO(BaseModel):
    projectTrackingId: Optional[str] = None
    orderSlip: Optional[bool] = None
    jobCard: Optional[bool] = None
    paperCutting: Optional[bool] = None
    platePreparation: Optional[bool] = None
    printing: Optional[bool] = None
    postPress: Optional[bool] = None
    delivery: Optional[bool] = None
    end: Optional[bool] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True
