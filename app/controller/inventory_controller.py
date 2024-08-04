from fastapi import APIRouter, HTTPException, Body, Depends
from app.service.inventory_service import InventoryService
from app.utils.response_util import get_response
from app.dto.inventory_dto import InventoryDTO
from app.models.inventory import InventoryItem, Items
from app.models.issued_item import IssuedItem
from app.dto.issued_item_dto import IssuedItemDTO
from app.dto.inventory_dto import ItemDTO
from typing import List
from app.utils.auth_utils import admin_verification

inventory_route = APIRouter()
inventory_service = InventoryService()

@inventory_route.post("/inventory", response_model=InventoryDTO)
async def create_inventory_item(inventory_data: InventoryDTO, payload: dict = Depends(admin_verification)):
    inventory_data_dict = inventory_data.dict(exclude_none=True)
    inventory_item = InventoryItem(**inventory_data_dict)
    created_inventory_item = await inventory_service.create_inventory_item(inventory_item)
    return get_response(status="success", message=created_inventory_item, status_code=201)

@inventory_route.get("/inventory/{inventoryId}", response_model=InventoryDTO)
async def get_inventory_item(inventoryId: str, payload: dict = Depends(admin_verification)):
    inventory_item = await inventory_service.get_inventory_item_by_id(inventoryId)
    return get_response(status="success", data=InventoryDTO(**inventory_item).dict(by_alias=True), status_code=200)

@inventory_route.get("/inventory", response_model=list[InventoryDTO])
async def get_all_inventory_items(payload: dict = Depends(admin_verification)):
    inventory_items = await inventory_service.get_all_inventory_items()
    return get_response(status="success", data=[InventoryDTO(**item).dict(by_alias=True) for item in inventory_items], status_code=200)

@inventory_route.post('/issued_item', response_model=IssuedItemDTO)
async def post_issued_items(issued: IssuedItemDTO, payload: dict = Depends(admin_verification)):
    created_item = await inventory_service.create_issued_item(IssuedItem(**issued.dict()))
    return get_response(status="success", message=created_item, status_code=201)

@inventory_route.put('/update-item/{inventoryId}/{itemId}')
async def update_availability(inventoryId: str, itemId: str, availability: int = Body(...), payload: dict = Depends(admin_verification)):
    updated_availability = await inventory_service.update_availability(inventoryId, itemId, availability)
    return get_response(status="success", message=updated_availability, status_code=201)

@inventory_route.post("/add-item/{inventoryId}")
async def add_item(inventoryId: str, item: List[ItemDTO], payload: dict = Depends(admin_verification)):
    item_data_dict = [item.dict(exclude_none=True) for item in item]
    created_items = [Items(**item_data) for item_data in item_data_dict]
    new_item_count = await inventory_service.add_itemType(inventoryId, created_items)
    return get_response(status="success", message=f"{new_item_count} items added", status_code=201)

@inventory_route.delete("/inventory/{itemId}")
async def delete_type(itemId: str, payload: dict = Depends(admin_verification)):
    response = await inventory_service.delete_type(itemId)
    return get_response(status="success", message=response, status_code=200)

@inventory_route.delete("/inventory/{inventoryId}/{itemId}")
async def delete_item(inventoryId: str, itemId: str, payload: dict = Depends(admin_verification)):
    response = await inventory_service.delete_item(inventoryId, itemId)
    return get_response(status="success", message=response, status_code=200)
