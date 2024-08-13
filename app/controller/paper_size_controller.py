# app/routes/paper_size_route.py
from fastapi import APIRouter, Depends, HTTPException
from app.dto.paper_size_dto import PaperSizeDTO, PaperSizeResponseDTO
from app.service.paper_size_service import PaperSizeService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification
from typing import List

paper_size_route = APIRouter()
paper_size_service = PaperSizeService()
logger = get_logger()

@paper_size_route.post("/paperSizes")
async def create_paper_size(paper_size: PaperSizeDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /paperSizes (POST) \n DATA SENT: {paper_size.dict()}")
    response = await paper_size_service.create_paper_size(paper_size)
    logger.info("RESPONSE SENT: Paper Size created successfully")
    return get_response(status="success", status_code=201, data=response)

@paper_size_route.get("/paperSizes")
async def get_all_paper_sizes() -> List[PaperSizeResponseDTO]:
    logger.info("ENDPOINT CALLED: /paperSizes (GET)")
    response = await paper_size_service.get_all_paper_sizes()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} paper size records")
    return get_response(status="success", status_code=200, data=response)

@paper_size_route.get("/paperSizes/{paper_size_id}")
async def get_paper_size_by_id(paper_size_id: str):
    logger.info(f"ENDPOINT CALLED: /paperSizes/{paper_size_id} (GET)")
    response = await paper_size_service.get_paper_size_by_id(paper_size_id)
    logger.info(f"RESPONSE SENT: Paper Size found with ID: {paper_size_id}")
    return get_response(status="success", status_code=200, data=response)

@paper_size_route.put("/paperSizes/{paper_size_id}")
async def update_paper_size(paper_size_id: str, paper_size_update: PaperSizeDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /paperSizes/{paper_size_id} (PUT) \n DATA SENT: {paper_size_update.dict()}")
    response = await paper_size_service.update_paper_size(paper_size_id, paper_size_update)
    logger.info(f"RESPONSE SENT: Paper Size record {paper_size_id} updated successfully")
    return get_response(status="success", status_code=200, data=response)

@paper_size_route.delete("/paperSizes/{paper_size_id}")
async def delete_paper_size(paper_size_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /paperSizes/{paper_size_id} (DELETE)")
    await paper_size_service.delete_paper_size(paper_size_id)
    logger.info(f"RESPONSE SENT: Paper Size record {paper_size_id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")