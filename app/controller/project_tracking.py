from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from app.dto.project_tracking_dto import ProjectTrackingDTO
from app.service.order_service import OrderService
from app.utils.auth_utils import admin_verification
from app.utils.response_util import get_response

project_tracking_router = APIRouter()

@project_tracking_router.get("/projectTracking/{order_id}", response_model=ProjectTrackingDTO)
async def get_project_tracking(
    order_id: str,
    current_admin: Dict = Depends(admin_verification),
    order_service: OrderService = Depends()
):
    try:
        project_tracking = await order_service.get_project_tracking(order_id)
        if not project_tracking:
            raise HTTPException(status_code=404, detail="Project tracking not found")
        return project_tracking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@project_tracking_router.put("/projectTracking/{order_id}")
async def update_project_tracking(
    order_id: str,
    project_tracking: ProjectTrackingDTO,
    current_admin: Dict = Depends(admin_verification),
    order_service: OrderService = Depends()
):
    try:
        updated_tracking = await order_service.update_project_tracking(order_id, project_tracking.dict())
        if not updated_tracking:
            raise HTTPException(status_code=404, detail="Order not found")
        return get_response(status="success",status_code=200,message="Project Tracking Updated")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

