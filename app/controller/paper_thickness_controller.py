# app/routes/paper_thickness_route.py
from fastapi import APIRouter, Depends, HTTPException
from app.dto.paper_thickness_dto import PaperThicknessDTO, PaperThicknessResponseDTO
from app.service.paper_thickness_service import PaperThicknessService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification
from typing import List

paper_thickness_route = APIRouter()
paper_thickness_service = PaperThicknessService()
logger = get_logger()

@paper_thickness_route.post("/paperThickness")
async def create_paper_thickness(paper_thickness: PaperThicknessDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /paperThickness (POST) \n DATA SENT: {paper_thickness.dict()}")
    response = await paper_thickness_service.create_paper_thickness(paper_thickness)
    logger.info("RESPONSE SENT: Paper Thickness created successfully")
    return get_response(status="success", status_code=201, data=response)

@paper_thickness_route.get("/paperThickness")
async def get_all_paper_thicknesses() -> List[PaperThicknessResponseDTO]:
    logger.info("ENDPOINT CALLED: /paperThickness (GET)")
    response = await paper_thickness_service.get_all_paper_thicknesses()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} paper thickness records")
    return get_response(status="success", status_code=200, data=response)

@paper_thickness_route.get("/paperThickness/{thickness_id}")
async def get_paper_thickness_by_id(thickness_id: str):
    logger.info(f"ENDPOINT CALLED: /paperThickness/{thickness_id} (GET)")
    response = await paper_thickness_service.get_paper_thickness_by_id(thickness_id)
    if response:
        logger.info(f"RESPONSE SENT: Paper Thickness found with ID: {thickness_id}")
    else:
        logger.warn(f"Paper Thickness with ID {thickness_id} not found")
    return get_response(status="success", status_code=200, data=response)

@paper_thickness_route.put("/paperThickness/{thickness_id}")
async def update_paper_thickness(thickness_id: str, paper_thickness_update: PaperThicknessDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /paperThickness/{thickness_id} (PUT) \n DATA SENT: {paper_thickness_update.dict()}")
    response = await paper_thickness_service.update_paper_thickness(thickness_id, paper_thickness_update)
    if response:
        logger.info(f"RESPONSE SENT: Paper Thickness record {thickness_id} updated successfully")
    else:
        logger.warn(f"Failed to update Paper Thickness with ID {thickness_id}")
    return get_response(status="success", status_code=200, data=response)

@paper_thickness_route.delete("/paperThickness/{thickness_id}")
async def delete_paper_thickness(thickness_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /paperThickness/{thickness_id} (DELETE)")
    await paper_thickness_service.delete_paper_thickness(thickness_id)
    logger.info(f"RESPONSE SENT: Paper Thickness record {thickness_id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")