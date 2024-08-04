from fastapi import APIRouter, Depends
from app.dto.leave_dto import LeaveDTO
from app.service.leave_service import LeaveService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification

leave_route = APIRouter()
leave_service = LeaveService()
logger = get_logger()

@leave_route.post("/leave/{staff_id}")
async def create_leave(staff_id: str, leave: LeaveDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /LEAVE/{staff_id} (POST) \n DATA SENT: {leave.dict()}")
    response = await leave_service.add_leave(staff_id, leave)
    logger.info(f"RESPONSE SENT: Leave created successfully for staff ID {staff_id}")
    return get_response(status="success", status_code=200, message=response)

@leave_route.get("/leave")
async def get_all_leaves(payload: dict = Depends(admin_verification)):
    logger.info("ENDPOINT CALLED: /LEAVE (GET)")
    response = await leave_service.get_all_leaves()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} leave records")
    return get_response(status="success", status_code=200, data=response)

@leave_route.put("/leave/{leave_id}")
async def update_leave(leave_id: str, leave_update: LeaveDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /LEAVE/{leave_id} (PUT) \n DATA SENT: {leave_update.dict()}")
    response = await leave_service.update_leave(leave_id, leave_update)
    logger.info(f"RESPONSE SENT: Leave record {leave_id} updated successfully")
    return get_response(status="success", status_code=200, message=response)

@leave_route.post("/leave/approve/{leave_id}")
async def approve_leave(leave_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /LEAVE/APPROVE/{leave_id} (POST)")
    response = await leave_service.approve_leave(leave_id)
    logger.info(f"RESPONSE SENT: Leave record {leave_id} approved successfully")
    return get_response(status="success", status_code=200, message=response)

@leave_route.post("/leave/reject/{leave_id}")
async def reject_leave(leave_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /LEAVE/REJECT/{leave_id} (POST)")
    response = await leave_service.reject_leave(leave_id)
    logger.info(f"RESPONSE SENT: Leave record {leave_id} rejected successfully")
    return get_response(status="success", status_code=200, message=response)

@leave_route.get("/leave/staff/{staff_id}")
async def get_leave_for_staff(staff_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /LEAVE/STAFF/{staff_id} (GET)")
    response = await leave_service.get_leave_by_staff_id(staff_id)
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} leave records for staff_id : {staff_id}")
    return get_response(status="success", status_code=200, data=response)

@leave_route.get("/auth/leave/staff")
async def get_leave_for_staff_by_token(payload: dict = Depends(staff_verification)):
    staff_id=payload.get("staff_id")
    logger.info(f"ENDPOINT CALLED: /LEAVE/STAFF/{staff_id} (GET)")
    response = await leave_service.get_leave_by_staff_id(staff_id)
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} leave records for staff_id : {staff_id}")
    return get_response(status="success", status_code=200, data=response)
