from pydantic import BaseModel, Field
from bson.dbref import DBRef
import json

class UserDTO(BaseModel): 
    fullName: str
    
    def from_user_collection(document: dict) -> 'UserDTO':
        return UserDTO (
            fullName=document.get("fullName")
        )
        
class CoverTreatmentDTO(BaseModel):
    coverTreatmentType: str
    
    def from_coverTreatment_collection(document: dict) -> 'CoverTreatmentDTO':
        return CoverTreatmentDTO (
            coverTreatmentType=document.get("coverTreatmentType")
        )
        
class PaperDTO(BaseModel):
    paperType: str
    
    def from_paper_collection(document: dict) -> 'PaperDTO':
        return PaperDTO (
            paperType=document.get("paperType")
            )