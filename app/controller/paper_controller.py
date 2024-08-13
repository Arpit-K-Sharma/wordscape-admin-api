# app/routes/paper_route.py
from fastapi import APIRouter, Depends, HTTPException
from app.dto.paper_dto import PaperDTO, PaperResponseDTO
from app.service.paper_service import PaperService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification
from typing import List

paper_route = APIRouter()
paper_service = PaperService()
logger = get_logger()

@paper_route.get("/papers")
async def get_all_papers() -> List[PaperResponseDTO]:
    logger.info("ENDPOINT CALLED: /papers (GET)")
    response = await paper_service.get_all_papers()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} paper records")
    return get_response(status="success", status_code=200, data=response)

@paper_route.post("/papers")
async def create_paper(paper: PaperDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /papers (POST) \n DATA SENT: {paper.dict()}")
    response = await paper_service.create_paper(paper)
    logger.info("RESPONSE SENT: Paper created successfully")
    return get_response(status="success", status_code=200, message="New Paper Added !!!")

@paper_route.put("/papers/{paper_id}")
async def update_paper(paper_id: str, paper_update: PaperDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /papers/{paper_id} (PUT) \n DATA SENT: {paper_update.dict()}")
    response = await paper_service.update_paper(paper_id, paper_update)
    logger.info(f"RESPONSE SENT: Paper record {paper_id} updated successfully")
    return get_response(status="success", status_code=200, message="Paper Updated !!!")

@paper_route.delete("/papers/{paper_id}")
async def delete_paper(paper_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /papers/{paper_id} (DELETE)")
    await paper_service.delete_paper(paper_id)
    logger.info(f"RESPONSE SENT: Paper record {paper_id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")