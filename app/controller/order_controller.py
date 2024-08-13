# app/routes/order_route.py
from fastapi import APIRouter, Depends, Query, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from typing import List, Optional
from datetime import datetime
from app.dto.order_dto import OrderDTO, OrderResponseDTO
from app.service.order_service import OrderService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification

order_route = APIRouter()
order_service = OrderService()
logger = get_logger()

@order_route.get("/orders", response_model=OrderResponseDTO)
async def get_all_orders(
    page_number: int = Query(0, ge=0),
    page_size: int = Query(10, ge=1, le=100),
    sort_field: str = Query("orderId", regex="^(date|deadline|orderId)$"),
    sort_direction: str = Query("desc", regex="^(asc|desc)$"),
    _: dict = Depends(admin_verification)
):
    logger.info(f"ENDPOINT CALLED: /orders (GET)")
    logger.info(f"PAGE NUMBER: {page_number}, PAGE SIZE: {page_size}, SORT FIELD: {sort_field}, SORT DIRECTION: {sort_direction}")
    orders = await order_service.get_all_orders(page_number, page_size, sort_field, sort_direction)
    logger.info(f"RESPONSE: {orders.total_elements} orders returned")
    return orders

@order_route.get("/orders/{order_id}", response_model=OrderDTO)
async def get_order_by_id(
    order_id: str,
    _: dict = Depends(admin_verification)
):
    logger.info(f"ENDPOINT CALLED: /orders/{order_id} (GET)")
    order = await order_service.get_order_by_id(order_id)
    logger.info(f"RESPONSE: Order found with ID: {order_id}")
    return order

@order_route.put("/orders/cancel/{order_id}", response_model=str)
async def cancel_order(
    order_id: str,
    _: dict = Depends(admin_verification)
):
    logger.info(f"ENDPOINT CALLED: /orders/cancel/{order_id} (PUT)")
    await order_service.cancel_order(order_id)
    logger.info(f"Order with ID {order_id} cancelled successfully")
    return get_response(status="success",status_code=200,message="Order Cancelled Successfully")


############ PDF DOWNLOAD ###########################

@order_route.get("/orders/invoice/{id}")
async def get_invoice_by_id(
    id: str,
    _: dict = Depends(admin_verification)
):
    try:
        invoice_data = await order_service.get_invoice_by_id(id)
        return invoice_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@order_route.get("/orders/{order_id}/filenames")
async def get_order_pdf_filename(order_id: str, payload = Depends(admin_verification)):
    try:
        pdf_filenames = await order_service.get_order_pdf_filenames(order_id)
        return get_response(status="success",status_code=200,data={"pdfFile":pdf_filenames})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@order_route.get("orders/file/{filename}")
async def get_pdf_by_filename(filename: str, payload = Depends(admin_verification)):
    try:
        pdf_file = await order_service.get_pdf_for_order(filename)
        return pdf_file
    except Exception as e:
        raise HTTPException(status_code=404, detail = str(e))
