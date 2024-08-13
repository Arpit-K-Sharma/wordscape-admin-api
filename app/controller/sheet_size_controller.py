from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.dto.sheet_size_dto import SheetSizeDTO, SheetSizeResponseDTO
from app.service.sheet_size_service import SheetSizeService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification

sheet_size_route = APIRouter()
sheet_size_service = SheetSizeService()
logger = get_logger()

@sheet_size_route.get("/sheetSizes")
async def get_all_sheet_sizes() -> List[SheetSizeResponseDTO]:
    logger.info("ENDPOINT CALLED: /sheetSizes (GET)")
    response = await sheet_size_service.get_all_sheet_sizes()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} sheet size records")
    return get_response(status="success", status_code=200, data=response)

@sheet_size_route.get("/sheetSizes/{id}")
async def get_sheet_size_by_id(id: str):
    logger.info(f"ENDPOINT CALLED: /sheetSizes/{id} (GET)")
    response = await sheet_size_service.get_sheet_size_by_id(id)
    if not response:
        raise HTTPException(status_code=404, detail="Sheet Size not found")
    logger.info(f"RESPONSE SENT: Sheet Size found with ID: {id}")
    return get_response(status="success", status_code=200, data=response)

@sheet_size_route.post("/sheetSizes")
async def create_sheet_size(sheet_size: SheetSizeDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /sheetSizes (POST) \n DATA SENT: {sheet_size.dict()}")
    response = await sheet_size_service.create_sheet_size(sheet_size)
    logger.info("RESPONSE SENT: Sheet Size created successfully")
    return get_response(status="success", status_code=201, message="Sheet Size Added")

@sheet_size_route.put("/sheetSizes/{id}")
async def update_sheet_size(id: str, sheet_size_update: SheetSizeDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /sheetSizes/{id} (PUT) \n DATA SENT: {sheet_size_update.dict()}")
    response = await sheet_size_service.update_sheet_size(id, sheet_size_update)
    if not response:
        raise HTTPException(status_code=404, detail="Sheet Size not found")
    logger.info(f"RESPONSE SENT: Sheet Size record {id} updated successfully")
    return get_response(status="success", status_code=200, message="Sheet Size Updated")

@sheet_size_route.delete("/sheetSizes/{id}")
async def delete_sheet_size(id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /sheetSizes/{id} (DELETE)")
    result = await sheet_size_service.delete_sheet_size(id)
    if not result:
        raise HTTPException(status_code=404, detail="Sheet Size not found")
    logger.info(f"RESPONSE SENT: Sheet Size record {id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")
