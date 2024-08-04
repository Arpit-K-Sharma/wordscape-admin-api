from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson.dbref import DBRef
import json
from bson import ObjectId


class ApprovedOrdersDTO(BaseModel):
    
    class Config:
        arbitrary_types_allowed = True
    
    id: Optional[str] = Field(alias='_id')
    date: Optional[str]
    paperSize: Optional[str]
    pages: Optional[int]
    quantity: Optional[int]
    binding: Optional[str]
    coverTreatment: Optional[str]
    innerPaper: Optional[str] 
    innerPaperThickness: Optional[int]
    outerPaper: Optional[str]
    outerPaperThickness: Optional[int]
    innerLamination: Optional[str]
    outerLamination: Optional[str]
    inkType: Optional[str]
    deliveryOption: Optional[str]
    status: Optional[str]
    customer: Optional[str]
    estimatedAmount: Optional[int]
    purchase_order_created: Optional[bool]
    
    @staticmethod
    def convert_objectid_to_str(oid):
        print(oid)
        if isinstance(oid, ObjectId):
            return str(oid)
        return None

    @staticmethod
    def convert_dbref_to_str(dbref):
        if isinstance(dbref, DBRef):
            return f"{dbref.id}"
        return None

    @staticmethod
    def convert_date(date_obj):
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
        return None

    @staticmethod
    def from_order_collection(document: dict) -> 'ApprovedOrdersDTO':
        print(document.get("_id"))
        return ApprovedOrdersDTO(
            _id=str(document.get("_id")),
            date=ApprovedOrdersDTO.convert_date(document.get("date")), 
            paperSize=document.get("paperSize"),
            pages=document.get("pages"),
            quantity=document.get("quantity"),
            binding=document.get("binding"),
            coverTreatment=ApprovedOrdersDTO.convert_dbref_to_str(document.get("coverTreatment")),  
            innerPaper=ApprovedOrdersDTO.convert_dbref_to_str(document.get("innerPaper")),  
            innerPaperThickness=document.get("innerPaperThickness"),
            outerPaper=ApprovedOrdersDTO.convert_dbref_to_str(document.get("outerPaper")),  
            outerPaperThickness=document.get("outerPaperThickness"),
            innerLamination=ApprovedOrdersDTO.convert_dbref_to_str(document.get("innerLamination")),  
            outerLamination=ApprovedOrdersDTO.convert_dbref_to_str(document.get("outerLamination")),  
            inkType=document.get("inkType"),
            deliveryOption=document.get("deliveryOption"),
            status=document.get("status"),
            customer=ApprovedOrdersDTO.convert_dbref_to_str(document.get("customer")),  
            estimatedAmount=document.get("estimatedAmount"),        
            purchase_order_created=document.get("purchase_order_created")
        )