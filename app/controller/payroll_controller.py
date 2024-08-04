from fastapi import APIRouter, Depends
from app.dto.payroll_dto import PayrollDTO
from app.service.payroll_service import PayrollService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification

payroll_route = APIRouter()
payroll_service = PayrollService()
logger = get_logger()

@payroll_route.post("/payroll")
async def generate_payroll(payload: dict = Depends(admin_verification)):
    logger.info("ENDPOINT CALLED: POST /payroll - Generating payroll")
    response = await payroll_service.generate_payroll()
    logger.info("Payroll generated successfully")
    return get_response(status="success", status_code=200, data=response)

@payroll_route.get("/payroll/{payroll_id}")
async def get_payroll(payroll_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: GET /payroll/{payroll_id} - Retrieving payroll")
    response = await payroll_service.get_payroll(payroll_id)
    logger.info(f"Payroll retrieved for ID: {payroll_id}")
    return get_response(status="success", status_code=200, data=response)

@payroll_route.put("/payroll/{payroll_id}")
async def update_payroll(payroll_id: str, payroll: PayrollDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: PUT /payroll/{payroll_id} - Updating payroll")
    response = await payroll_service.update_calculated_payroll(payroll_id, payroll)
    logger.info(f"Payroll updated for ID: {payroll_id}")
    return get_response(status="success", status_code=200, message=response)

@payroll_route.delete("/payroll/{payroll_id}")
async def delete_payroll(payroll_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: DELETE /payroll/{payroll_id} - Deleting payroll")
    response = await payroll_service.delete_payroll(payroll_id)
    logger.info(f"Payroll deleted for ID: {payroll_id}")
    return get_response(status="success", status_code=200, message=response)

@payroll_route.get("/payroll")
async def list_payrolls(payload: dict = Depends(admin_verification)):
    logger.info("ENDPOINT CALLED: GET /payroll - Listing all payrolls")
    response = await payroll_service.list_all_payrolls()
    logger.info(f"Retrieved {len(response)} payroll records")
    return get_response(status="success", status_code=200, data=response)

@payroll_route.get("/payroll/month/{month}")
async def get_payroll_by_month(month: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: GET /payroll/month/{month} - Retrieving payroll for month")
    response = await payroll_service.get_payroll_by_month(month)
    logger.info(f"Payroll retrieved for month: {month}")
    return get_response(status="success", status_code=200, data=response)

@payroll_route.delete("/payroll")
async def delete_all_payroll(payload: dict = Depends(admin_verification)):
    logger.info("ENDPOINT CALLED: DELETE /payroll - Deleting all payrolls")
    response = await payroll_service.delete_all_payroll()
    logger.info("All payroll records deleted")
    return get_response(status="success", status_code=200, message=response)

@payroll_route.get("/payroll/staff/{staff_id}")
async def get_payroll_for_staff(staff_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /PAYROLL/STAFF/{staff_id} (GET)")
    response = await payroll_service.get_payroll_by_staff_id(staff_id)
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} payroll records for staff_id : {staff_id}")
    return get_response(status="success", status_code=200, data=response)

@payroll_route.get("/auth/payroll/staff")
async def get_payroll_for_staff_by_token(payload: dict = Depends(staff_verification)):
    staff_id=payload.get("staff_id")
    logger.info(f"ENDPOINT CALLED: /PAYROLL/STAFF/{staff_id} (GET)")
    response = await payroll_service.get_payroll_by_staff_id(staff_id)
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} payroll records for staff_id : {staff_id}")
    return get_response(status="success", status_code=200, data=response)
