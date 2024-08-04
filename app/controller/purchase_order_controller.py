from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.models.purchase_order import PurchaseOrder
from app.service.purchase_order_service import PurchaseOrderService
from app.repository.purchase_order_repository import PurchaseOrderRepository
from app.dto.purchase_order_dto import PurchaseOrderDTO
from app.dto.purchase_entry_dto import PurchaseEntryDTO
from app.models.purchase_entry import PurchaseEntry
from app.service.reorder_service import ReorderService
from typing import List
from app.utils.response_util import get_response
from app.service.file_service import FileService
from app.utils.auth_utils import admin_verification

purchase_order_route = APIRouter()
purchase_order_repository = PurchaseOrderRepository()
purchase_order_service = PurchaseOrderService(purchase_order_repository)

@purchase_order_route.post("/purchase_order", response_description="Add new purchase order", response_model=PurchaseOrderDTO)
async def create_purchase_order(purchase_order_data: PurchaseOrderDTO, payload: dict = Depends(admin_verification)):
    await purchase_order_service.create_purchase_order(PurchaseOrder(**purchase_order_data.dict(exclude_none=True)))
    return get_response(status="success", message="Purchase Order Placed", status_code=201)

@purchase_order_route.get("/purchase_order/{order_id}", response_description="Get a purchase order", response_model=PurchaseOrderDTO)
async def get_purchase_order(order_id: str, payload: dict = Depends(admin_verification)):
    purchase_order = await purchase_order_service.get_purchase_order_by_id(order_id)
    return get_response(status="success", data=PurchaseOrderDTO(**purchase_order).dict(by_alias=True), status_code=200)

@purchase_order_route.put("/purchase_order/{purchase_order}", response_model=PurchaseOrderDTO)
async def update_purchase_order(purchase_order: str,  purchase_order_data: PurchaseOrderDTO, payload: dict = Depends(admin_verification)):
    await purchase_order_service.update_purchase_order(purchase_order_data.dict(exclude_unset=True), purchase_order)
    return get_response(status="success", message="Purchase Order Updated", status_code=200)

@purchase_order_route.get("/purchase_orders_without_entries", response_description="Get all purchase orders without entries", response_model=List[PurchaseOrderDTO])
async def get_purchase_orders_without_entries(payload: dict = Depends(admin_verification)):
    purchase_orders = await purchase_order_service.get_purchase_orders_without_entries()
    print(purchase_orders)
    return get_response(status="success", data=[PurchaseOrderDTO(**purchase_order).dict(by_alias=True) for purchase_order in purchase_orders], status_code=200)

@purchase_order_route.get("/purchase_orders_with_entries", response_description="Get all purchase orders with entries", response_model=List[PurchaseOrderDTO])
async def get_purchase_orders_with_entries(payload: dict = Depends(admin_verification)):
    purchase_orders = await purchase_order_service.get_purchase_orders_with_entries()
    return get_response(status="success", data=[PurchaseOrderDTO(**purchase_order).dict(by_alias=True) for purchase_order in purchase_orders], status_code=200)

@purchase_order_route.post("/purchase_entry/{order_id}", response_model=PurchaseEntryDTO)
async def create_purchase_entry(order_id: str, purchase_entry_data: PurchaseEntryDTO, payload: dict = Depends(admin_verification)):
    await purchase_order_service.create_purchase_entry(PurchaseEntry(**purchase_entry_data.dict()), order_id)
    return get_response(status="success", message="Purchase Entry Created", status_code=201)

@purchase_order_route.get("/reorders")
async def get_reorders(payload: dict = Depends(admin_verification)):
    purchase_orders = await purchase_order_service.get_reorder_entries()
    return get_response(
        status="success",
        data=[PurchaseOrderDTO(**purchase_order.dict()).dict(by_alias=True) for purchase_order in purchase_orders],
        status_code=200
    )

@purchase_order_route.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), payload: dict = Depends(admin_verification)):
    try:
        result = await FileService.save_uploaded_file(file)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
