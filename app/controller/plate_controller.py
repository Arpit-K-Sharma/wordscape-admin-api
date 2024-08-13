# app/routes/plate_route.py
from fastapi import APIRouter, Depends, HTTPException
from app.dto.plate_dto import PlateDTO, PlateResponseDTO
from app.service.plate_service import PlateService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification
from typing import List

plate_route = APIRouter()
plate_service = PlateService()
logger = get_logger()

@plate_route.get("/plates")
async def get_all_plates() -> List[PlateResponseDTO]:
    logger.info("ENDPOINT CALLED: /plates (GET)")
    response = await plate_service.get_all_plates()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} plate records")
    return get_response(status="success", status_code=200, data=response)

@plate_route.post("/plates")
async def create_plate(plate: PlateDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /plates (POST) \n DATA SENT: {plate.dict()}")
    response = await plate_service.create_plate(plate)
    logger.info("RESPONSE SENT: Plate created successfully")
    return get_response(status="success", status_code=200, message="New Plate Added !!!")

@plate_route.put("/plates/{plate_id}")
async def update_plate(plate_id: str, plate_update: PlateDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /plates/{plate_id} (PUT) \n DATA SENT: {plate_update.dict()}")
    response = await plate_service.update_plate(plate_id, plate_update)
    logger.info(f"RESPONSE SENT: Plate record {plate_id} updated successfully")
    return get_response(status="success", status_code=200, message="Plate Updated !!!")

@plate_route.delete("/plates/{plate_id}")
async def delete_plate(plate_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /plates/{plate_id} (DELETE)")
    await plate_service.delete_plate(plate_id)
    logger.info(f"RESPONSE SENT: Plate record {plate_id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")