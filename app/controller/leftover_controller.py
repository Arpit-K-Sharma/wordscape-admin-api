from fastapi import APIRouter, Depends
from typing import List
from app.dto.leftover_dto import LeftoverDTO, UpdateItemDTO
from app.service.leftover_service import LeftoverService
from app.utils.auth_utils import admin_verification

left_over_router = APIRouter()

@left_over_router.post("/leftovers")
async def create_leftover(leftover: LeftoverDTO, service: LeftoverService = Depends(), payload: dict = Depends(admin_verification)):
    return await service.create_leftover(leftover)

@left_over_router.get("/leftovers")
async def get_all_leftovers(service: LeftoverService = Depends(), payload: dict = Depends(admin_verification)):
    return await service.get_all_leftovers()

@left_over_router.get("/leftovers/{order_id}")
async def get_individual_leftovers(order_id: str, service: LeftoverService = Depends(), payload: dict = Depends(admin_verification)):
    return await service.get_individual_leftovers(order_id)

@left_over_router.put("/leftovers/{leftover_id}/items")
async def update_leftover_item(leftover_id: str, item: UpdateItemDTO, service: LeftoverService = Depends(), payload: dict = Depends(admin_verification)):
    return await service.update_leftover_item(leftover_id, item)
