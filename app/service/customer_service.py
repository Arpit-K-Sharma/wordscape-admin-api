# app/service/customer_service.py
from typing import List, Tuple
from fastapi import HTTPException
from app.repository.customer_repository import CustomerRepository
from app.dto.customer_dto import CustomerDTO, CustomerResponseDTO

class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    async def get_all_customers(self, skip: int, limit: int, sort_field: str, sort_direction: str) -> Tuple[List[CustomerResponseDTO], int]:
        customers, total_elements = await self.repository.find_all_customers(skip=skip, limit=limit, sort_field=sort_field, sort_direction=sort_direction)
        return [CustomerResponseDTO(**customer) for customer in customers], total_elements

    async def deactivate_customer(self, customer_id: str) -> CustomerResponseDTO:
        customer = await self.repository.find_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        customer['status'] = False
        updated_customer = await self.repository.update_customer(customer_id, customer)
        return CustomerResponseDTO(**updated_customer)

    async def reactivate_customer(self, customer_id: str) -> CustomerResponseDTO:
        customer = await self.repository.find_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        customer['status'] = True
        updated_customer = await self.repository.update_customer(customer_id, customer)
        return CustomerResponseDTO(**updated_customer)