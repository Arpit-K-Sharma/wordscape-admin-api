# app/routes/binding_route.py
from fastapi import APIRouter, Depends, HTTPException
from app.dto.binding_dto import BindingDTO, BindingResponseDTO
from app.service.binding_service import BindingService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification

binding_route = APIRouter()
binding_service = BindingService()
logger = get_logger()

@binding_route.get("/bindings")
async def get_all_bindings():
    logger.info("ENDPOINT CALLED: /bindings (GET)")
    response = await binding_service.get_all_bindings()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} binding records")
    return get_response(status="success", status_code=200, data=response)

@binding_route.post("/bindings")
async def create_binding(binding: BindingDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /bindings (POST) \n DATA SENT: {binding.dict()}")
    response = await binding_service.create_binding(binding)
    logger.info("RESPONSE SENT: Binding created successfully")
    return get_response(status="success", status_code=200, message="Binding Added!!")

@binding_route.put("/bindings/{binding_id}")
async def update_binding(binding_id: str, binding_update: BindingDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /bindings/{binding_id} (PUT) \n DATA SENT: {binding_update.dict()}")
    response = await binding_service.update_binding(binding_id, binding_update)
    logger.info(f"RESPONSE SENT: Binding record {binding_id} updated successfully")
    return get_response(status="success", status_code=200, message="Binding Updated !!!")

@binding_route.delete("/bindings/{binding_id}")
async def delete_binding(binding_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /bindings/{binding_id} (DELETE)")
    await binding_service.delete_binding(binding_id)
    logger.info(f"RESPONSE SENT: Binding record {binding_id} deleted successfully")
    return get_response(status="success", status_code=204, message="Deleted Successfully !!!")