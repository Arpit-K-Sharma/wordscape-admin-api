# app/routes/customer_route.py
from fastapi import APIRouter, Depends, Query
from typing import List
from app.dto.customer_dto import CustomerDTO, CustomerListResponseDTO, CustomerResponseDTO
from app.service.customer_service import CustomerService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification, staff_verification

customer_route = APIRouter()
customer_service = CustomerService()
logger = get_logger()

@customer_route.get("/customers", response_model=CustomerListResponseDTO)
async def get_all_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_field: str = Query("id", regex="^(id|fullName|email)$"),
    sort_direction: str = Query("asc", regex="^(asc|desc)$"),
    payload: dict = Depends(admin_verification)
):
    logger.info(f"ENDPOINT CALLED: /customers (GET) with params: skip={skip}, limit={limit}, sort_field={sort_field}, sort_direction={sort_direction}")
    customers, total_elements = await customer_service.get_all_customers(skip=skip, limit=limit, sort_field=sort_field, sort_direction=sort_direction)
    logger.info(f"RESPONSE SENT: Retrieved {total_elements} customer records")
    return CustomerListResponseDTO(customers=customers, total_elements=total_elements)

@customer_route.put("/customers/{customer_id}/deactivate", response_model=CustomerResponseDTO)
async def deactivate_customer(customer_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /customers/{customer_id}/deactivate (PUT)")
    response = await customer_service.deactivate_customer(customer_id)
    logger.info(f"RESPONSE SENT: Customer {customer_id} deactivated successfully")
    return get_response(status="success", status_code=200, data=response, message="Customer Deactivated !!!")

@customer_route.put("/customers/{customer_id}/reactivate", response_model=CustomerResponseDTO)
async def reactivate_customer(customer_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /customers/{customer_id}/reactivate (PUT)")
    response = await customer_service.reactivate_customer(customer_id)
    logger.info(f"RESPONSE SENT: Customer {customer_id} reactivated successfully")
    return get_response(status="success", status_code=200, data=response, message="Customer Reactivated !!!")