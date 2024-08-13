from fastapi import APIRouter, FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from app.repository.order_repository import OrderRepository

from app.service.job_card_service import JobCardService
from app.utils.auth_utils import admin_verification

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

job_card_service = JobCardService(OrderRepository())

jobCard_route = APIRouter()

@jobCard_route.post("/jobCard/{order_id}")
async def create_job_card(order_id: str, job_card_data: Dict, current_user: Dict = Depends(admin_verification)):
    try:
        await job_card_service.create_job_card(order_id, job_card_data)
        return {"message": "JobCard Added !!!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@jobCard_route.put("/jobCard/update/{order_id}")
async def update_job_card(order_id: str, job_card_data: Dict, current_user: Dict = Depends(admin_verification)):
    if "ROLE_ADMIN" not in current_user["roles"] and "ROLE_USER" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        job_card_service.update_job_card(order_id, job_card_data)
        return {"message": "JobCard Updated !!!"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@jobCard_route.put("/jobCard/updateDeadline/{order_id}")
async def update_deadline(order_id: str, deadline: Dict, current_user: Dict = Depends(admin_verification)):
    try:
        job_card_service.update_deadline(order_id, deadline["deadline"])
        return {"message": "Deadline Updated"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@jobCard_route.get("/jobCard/{order_id}")
async def get_job_card(order_id: str, current_user: Dict = Depends(admin_verification)):
    try:
        return await job_card_service.get_job_card_by_id(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))