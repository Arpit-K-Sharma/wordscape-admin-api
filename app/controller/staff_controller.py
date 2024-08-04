from fastapi import APIRouter, Depends
from app.dto.staff_dto import StaffDTO, StaffResponseDTO  
from app.service.staff_service import StaffService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification

staff_route = APIRouter()
staff_service = StaffService()
logger = get_logger()

@staff_route.post("/staff", dependencies=[Depends(admin_verification)])
async def create_staff(staff: StaffDTO):
    logger.info(f"ENDPOINT CALLED: POST /staff - Creating new staff")
    response = await staff_service.add_staff(staff)
    logger.info(f"Staff created successfully. ID: {response}")
    return get_response(status="success", status_code=200, message=response)

@staff_route.put("/staff/{staff_id}", dependencies=[Depends(admin_verification)])
async def update_staff(staff_id: str, staff: StaffDTO):
    logger.info(f"ENDPOINT CALLED: PUT /staff/{staff_id} - Updating staff")
    response = await staff_service.update_staff(staff_id, staff)
    logger.info(f"Staff updated successfully. ID: {staff_id}")
    return get_response(status="success", status_code=200, message=response)

@staff_route.get("/staff", response_model=list[StaffResponseDTO], dependencies=[Depends(admin_verification)], )
async def get_all_staff():
    logger.info("ENDPOINT CALLED: GET /staff - Retrieving all staff")
    response = await staff_service.get_all_staff()
    logger.info(f"Retrieved {len(response)} staff members")
    return get_response(status="success", status_code=200, data=response)

@staff_route.get("/staff/{staff_id}", response_model=StaffResponseDTO, dependencies=[Depends(admin_verification)])
async def get_staff_by_id(staff_id: str):
    logger.info(f"ENDPOINT CALLED: GET /staff/{staff_id} - Retrieving staff by ID")
    response = await staff_service.get_staff_by_id(staff_id)
    logger.info(f"Staff retrieved successfully. ID: {staff_id}")
    return get_response(status="success", status_code=200, data=response)

@staff_route.get("/auth/staff", response_model=StaffResponseDTO)
async def get_staff_by_token(payload: dict = Depends(staff_verification)):
    staff_id = payload.get("staff_id")
    logger.info(f"ENDPOINT CALLED: GET /staff/{staff_id} - Retrieving staff by ID")
    response = await staff_service.get_staff_by_id(staff_id)
    logger.info(f"Staff retrieved successfully. ID: {staff_id}")
    return get_response(status="success", status_code=200, data=response)

@staff_route.delete("/staff/{staff_id}", dependencies=[Depends(admin_verification)])
async def delete_staff(staff_id: str):
    logger.info(f"ENDPOINT CALLED: DELETE /staff/{staff_id} - Deleting staff")
    response = await staff_service.delete_staff(staff_id)
    logger.info(f"Staff deleted successfully. ID: {staff_id}")
    return get_response(status="success", status_code=200, message=response)

@staff_route.get("/staff/department/{department_id}", response_model=list[StaffResponseDTO], dependencies=[Depends(admin_verification)])
async def get_staff_by_department_id(department_id: str):
    logger.info(f"ENDPOINT CALLED: GET /staff/department/{department_id} - Retrieving staff by department")
    response = await staff_service.find_staff_by_department_id(department_id)
    logger.info(f"Retrieved {len(response)} staff members for department {department_id}")
    return get_response(status="success", status_code=200, data=response)

@staff_route.get("/staff/activeStaffs", response_model=list[StaffDTO], dependencies=[Depends(admin_verification)])
async def get_active_staffs():
    logger.info("ENDPOINT CALLED: GET /staff/activeStaffs - Retrieving active staff")
    response = await staff_service.get_active_staffs()
    logger.info(f"Retrieved {len(response)} active staff members")
    return get_response(status="success", status_code=200, data=response)

@staff_route.post("/staff/deactivate/{staff_id}", dependencies=[Depends(admin_verification)])
async def deactivate_staff(staff_id: str):
    logger.info(f"ENDPOINT CALLED: POST /staff/deactivate/{staff_id} - Deactivating staff")
    response = await staff_service.deactivate_staff(staff_id)
    logger.info(f"Staff deactivated successfully. ID: {staff_id}")
    return get_response(status="success", status_code=200, message=response)

@staff_route.post("/staff/reactivate/{staff_id}", dependencies=[Depends(admin_verification)])
async def reactivate_staff(staff_id: str):
    logger.info(f"ENDPOINT CALLED: POST /staff/reactivate/{staff_id} - Reactivating staff")
    response = await staff_service.reactivate_staff(staff_id)
    logger.info(f"Staff reactivated successfully. ID: {staff_id}")
    return get_response(status="success", status_code=200, message=response)
