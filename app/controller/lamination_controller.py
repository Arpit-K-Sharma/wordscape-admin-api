# app/routes/lamination_route.py
from fastapi import APIRouter, Depends, HTTPException
from app.dto.lamination_dto import LaminationDTO, LaminationResponseDTO
from app.service.lamination_service import LaminationService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification
from typing import List

lamination_route = APIRouter()
lamination_service = LaminationService()
logger = get_logger()

@lamination_route.get("/laminations")
async def get_all_laminations() -> List[LaminationResponseDTO]:
    logger.info("ENDPOINT CALLED: /laminations (GET)")
    response = await lamination_service.get_all_laminations()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} lamination records")
    return get_response(status="success", status_code=200, data=response)

@lamination_route.post("/laminations")
async def create_lamination(lamination: LaminationDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /laminations (POST) \n DATA SENT: {lamination.dict()}")
    response = await lamination_service.create_lamination(lamination)
    logger.info("RESPONSE SENT: Lamination created successfully")
    return get_response(status="success", status_code=200, message="New Lamination Added !!!")

@lamination_route.put("/laminations/{lamination_id}")
async def update_lamination(lamination_id: str, lamination_update: LaminationDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /laminations/{lamination_id} (PUT) \n DATA SENT: {lamination_update.dict()}")
    response = await lamination_service.update_lamination(lamination_id, lamination_update)
    logger.info(f"RESPONSE SENT: Lamination record {lamination_id} updated successfully")
    return get_response(status="success", status_code=200, message="Lamination Updated !!!")

@lamination_route.delete("/laminations/{lamination_id}")
async def delete_lamination(lamination_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /laminations/{lamination_id} (DELETE)")
    await lamination_service.delete_lamination(lamination_id)
    logger.info(f"RESPONSE SENT: Lamination record {lamination_id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")