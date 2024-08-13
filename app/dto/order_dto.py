from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from bson.dbref import DBRef
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETE"
    CANCELED = "CANCELED"

class Orientation(str, Enum):
    PORTRAIT = "PORTRAIT"
    LANDSCAPE = "LANDSCAPE"

class OrderDTO(BaseModel):
    orderId: Optional[str] = None  # Changed from Field(None, alias='_id')
    date: Optional[str] = None
    deadline: Optional[str] = None
    paperSize: Optional[str] = None
    pages: Optional[int] = None
    quantity: Optional[int] = None
    bindingType: Optional[List[str]] = None
    innerPaperType: Optional[str] = None
    innerPaperThickness: Optional[int] = None
    outerPaperType: Optional[str] = None
    outerPaperThickness: Optional[int] = None
    innerLamination: Optional[str] = None
    outerLamination: Optional[str] = None
    inkType: Optional[List[str]] = None
    deliveryOption: Optional[str] = None
    remarks: Optional[str] = None
    companyName: Optional[str] = None
    address: Optional[str] = None
    orientation: Optional[Orientation] = None
    status: Optional[OrderStatus] = None
    customer: Optional[str] = None
    pdfFile: Optional[List[str]] = None
    bindingRate: Optional[float] = None
    innerPaperRate: Optional[float] = None
    outerPaperRate: Optional[float] = None
    innerLaminationRate: Optional[float] = None
    outerLaminationRate: Optional[float] = None
    plateRate: Optional[float] = None
    estimatedAmount: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def convert_objectid_to_str(oid):
        if isinstance(oid, ObjectId):
            return str(oid)
        return None

    @staticmethod
    def convert_dbref_to_str(dbref):
        if isinstance(dbref, DBRef):
            return str(dbref.id)
        return None

    @staticmethod
    def convert_date(date_obj):
        if isinstance(date_obj, datetime):
            return date_obj.isoformat()
        return None

    @staticmethod
    def from_order_collection(document: dict) -> 'OrderDTO':
        return OrderDTO(
            orderId=OrderDTO.convert_objectid_to_str(document.get("_id")),  # Changed from _id to orderId
            date=OrderDTO.convert_date(document.get("date")),
            deadline=OrderDTO.convert_date(document.get("deadline")),
            paperSize=document.get("paperSize"),
            pages=document.get("pages"),
            quantity=document.get("quantity"),
            bindingType=document.get("bindingType"),
            innerPaperType=document.get("innerPaperType"),
            innerPaperThickness=document.get("innerPaperThickness"),
            outerPaperType=document.get("outerPaperType"),
            outerPaperThickness=document.get("outerPaperThickness"),
            innerLamination=document.get("innerLamination"),
            outerLamination=document.get("outerLamination"),
            inkType=document.get("inkType"),
            orientation=document.get("orientation"),
            status=document.get("status"),
            customer=document.get("customer"),
            pdfFile=document.get("pdfFilename"),
            bindingRate=float(document.get("bindingRate", 0)),
            innerPaperRate=float(document.get("innerPaperRate", 0)),
            outerPaperRate=float(document.get("outerPaperRate", 0)),
            innerLaminationRate=float(document.get("innerLaminationRate", 0)),
            outerLaminationRate=float(document.get("outerLaminationRate", 0)),
            plateRate=float(document.get("plateRate", 0)),
            estimatedAmount=document.get("estimatedAmount")
        )

class OrderResponseDTO(BaseModel):
    orders: Optional[List[OrderDTO]] = None
    total_elements: Optional[int] = None
