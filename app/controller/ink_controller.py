from fastapi import APIRouter, Depends, HTTPException
from app.dto.ink_dto import InkDTO, InkResponseDTO
from app.service.ink_service import InkService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification

ink_route = APIRouter()
ink_service = InkService()
logger = get_logger()

@ink_route.get("/inks")
async def get_all_inks():
    logger.info("ENDPOINT CALLED: /inks (GET)")
    response = await ink_service.get_all_inks()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} ink records")
    return get_response(status="success", status_code=200, data=response)

@ink_route.post("/inks")
async def create_ink(ink: InkDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /inks (POST) \n DATA SENT: {ink.dict()}")
    response = await ink_service.create_ink(ink)
    logger.info("RESPONSE SENT: Ink created successfully")
    return get_response(status="success", status_code=201, message="Ink Added!!")

@ink_route.get("/inks/{ink_id}")
async def get_ink_by_id(ink_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /inks/{ink_id} (GET)")
    response = await ink_service.get_ink_by_id(ink_id)
    logger.info(f"RESPONSE SENT: Retrieved ink record for id {ink_id}")
    return get_response(status="success", status_code=200, data=response)

@ink_route.put("/inks/{ink_id}")
async def update_ink(ink_id: str, ink_update: InkDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /inks/{ink_id} (PUT) \n DATA SENT: {ink_update.dict()}")
    response = await ink_service.update_ink(ink_id, ink_update)
    logger.info(f"RESPONSE SENT: Ink record {ink_id} updated successfully")
    return get_response(status="success", status_code=200, message = "Ink Updated Successfully")

@ink_route.delete("/inks/{ink_id}")
async def delete_ink(ink_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /inks/{ink_id} (DELETE)")
    await ink_service.delete_ink(ink_id)
    logger.info(f"RESPONSE SENT: Ink record {ink_id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")