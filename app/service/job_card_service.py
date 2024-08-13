import uuid
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from app.repository.order_repository import OrderRepository
from app.service.order_service import OrderService

class JobCardService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo
        self.order_service = OrderService()

    async def create_job_card(self, order_id: str, job_card_data: dict):
        order = await self.order_repo.find_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found!")

        # Generate a random 4-digit job card ID
        job_card_id = str(uuid.uuid4())[:4]
        job_card_data["job_card_id"] = job_card_id

        # Combine job_card_data with the order dictionary
        order.update(job_card_data)

        # Update the status
        order["status"] = "APPROVED"

        # Update the projectTracking.job_card field
        if "projectTracking" not in order:
            order["projectTracking"] = {}
        order["projectTracking"]["jobCard"] = True

        # Save the updated order
        self.order_repo.save(order)

        return job_card_data


    async def get_job_card_by_id(self, order_id: str):
        order = await self.order_repo.find_job_card_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order Not found")
        
        enriched_order = await self.order_service.enrich_order_data_for_job_card(order)
        
        if "customer" in enriched_order:
            if "password" in enriched_order["customer"]:
                del enriched_order["customer"]["password"]
            
            # Convert customer._id to string and rename to customerId
            if "_id" in enriched_order["customer"]:
                enriched_order["customer"]["customerId"] = str(enriched_order["customer"].pop("_id"))
        
        # Convert ObjectId to string and rename "_id" to "orderId"
        if "_id" in enriched_order:
            enriched_order["orderId"] = str(enriched_order.pop("_id"))
        
        return enriched_order


    async def update_job_card(self, order_id: str, job_card_data: dict):
        order = await self.order_repo.find_order_by_id(order_id)
        if not order:
            raise ValueError("Order Not Found !!!")

        # Update order with new job card data
        order.update(job_card_data)
        self.order_repo.save(order)

    async def update_deadline(self, order_id: str, deadline: str):
        order = await self.order_repo.find_order_by_id(order_id)
        if not order:
            raise ValueError("Order Not Found")

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            order["deadline"] = deadline_date
            self.order_repo.save(order)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")