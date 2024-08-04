from fastapi import APIRouter, Depends, HTTPException
from app.service.approved_orders_services import ApprovedOrdersService
from app.utils.auth_utils import admin_verification

approved_orders_route = APIRouter()

@approved_orders_route.get('/get/approved_orders')
async def get_approved_orders(payload: dict = Depends(admin_verification)):
    response = await ApprovedOrdersService.fetch_all_approved_orders()
    return {"message": "Approved Orders Fetched Successfully", "data": response}
