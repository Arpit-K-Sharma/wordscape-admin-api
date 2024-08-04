from fastapi import APIRouter, HTTPException, Depends
from app.service.reorder_service import ReorderService
from app.dto.purchase_order_dto import PurchaseEntryDTO
from app.models.purchase_order import PurchaseEntry
from app.utils.response_util import get_response
from app.utils.auth_utils import admin_verification

re_order = APIRouter()
reorder_service = ReorderService()

@re_order.post('/reOrder/{order_id}', response_model=PurchaseEntryDTO)
async def post_reorder(order_id: str, reorder_data: PurchaseEntryDTO, payload: dict = Depends(admin_verification)):
    reorder_item = PurchaseEntry(**reorder_data.dict())
    await reorder_service.create_reorder(reorder_item, order_id)
    return get_response(status="success", message="Reorder Issued", status_code=200)
