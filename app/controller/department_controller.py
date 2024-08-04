from fastapi import APIRouter, Depends, HTTPException
from app.service.department_service import DepartmentService
from app.dto.department_dto import DepartmentDTO
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification

department_route = APIRouter()
department_service = DepartmentService()
logger = get_logger()

@department_route.post("/department")
async def add_department(department: DepartmentDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /DEPARTMENT (POST) \n DATA SENT: {department.dict()}")
    response = await department_service.add_department(department)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@department_route.put("/department/{department_id}")
async def update_department(department_id: str, department: DepartmentDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /DEPARTMENT/{department_id} (PUT) \n DATA SENT: {department.dict()}")
    response = await department_service.update_department(department_id, department)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@department_route.get("/department", response_model=list[DepartmentDTO])
async def get_all_departments(payload: dict = Depends(admin_verification)):
    logger.info("ENDPOINT CALLED: /DEPARTMENT (GET)")
    response = await department_service.get_all_departments()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} departments")
    return get_response(status="success", status_code=200, data=response)

@department_route.get("/department/name/{department_name}", response_model=DepartmentDTO)
async def get_by_department_name(department_name: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /DEPARTMENT/NAME/{department_name} (GET)")
    response = await department_service.get_by_department_name(department_name)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, data=response)

@department_route.get("/department/id/{department_id}", response_model=DepartmentDTO)
async def get_by_department_id(department_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /DEPARTMENT/ID/{department_id} (GET)")
    response = await department_service.get_by_department_id(department_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, data=response)

@department_route.delete("/department/{department_id}")
async def delete_department(department_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /DEPARTMENT/{department_id} (DELETE)")
    response = await department_service.delete_department(department_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)
