# app/repository/order_repository.py
from typing import List, Dict, Any
from bson import ObjectId
from app.config.db_config import database
from app.dto.order_dto import OrderDTO, OrderStatus

class OrderRepository:
    def __init__(self):
        self.collection = database["order"]
        self.paper_collection = database["paper"]
        self.lamination_collection = database["lamination"]
        self.customer_collection = database["user"]

    async def find_all_orders(self, skip: int, limit: int, sort_field: str, sort_direction: int) -> List[Dict[str, Any]]:
        sort_direction = 1 if sort_direction == "asc" else -1
        cursor = self.collection.find().skip(skip).limit(limit).sort(sort_field, sort_direction)
        return await cursor.to_list(length=None)
    
    async def find_order_by_id(self, order_id: str) -> Dict[str, Any]:
        return await self.collection.find_one({"_id": ObjectId(order_id)})
    
    async def count_orders(self) -> int:
        return await self.collection.count_documents({})
    
    async def cancel_order(self, order_id: str):
        return await self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": OrderStatus.CANCELED}}
        )
    
#################### PROJECT TRACKING #########################################
    async def update_project_tracking(self, order_id: str, tracking_data: Dict[str, bool]) -> Dict[str, Any]:
        # Ensure the order_id is valid
        if not ObjectId.is_valid(order_id):
            raise ValueError("Invalid order_id")

        # Perform the update operation
        result = await self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"projectTracking": tracking_data}}
        )

        # Check if the update was successful
        if result.matched_count == 0:
            raise ValueError(f"Order with id {order_id} not found")

        # Fetch and return the updated order
        updated_order = await self.find_order_by_id(order_id)
        return updated_order
    
########################## JOB CARD ########################################

    async def find_job_card_by_id(self, order_id: str) -> dict:
        return await self.collection.find_one({"_id": ObjectId(order_id)})

    def save(self, order: dict):
        if "_id" in order and order["_id"]:
            self.collection.update_one({"_id": order["_id"]}, {"$set": order})
        else:
            result = self.collection.insert_one(order)
            order["_id"] = result.inserted_id
        return order




    

############################## HELPER METHOD FOR ORDER ####################################
    async def get_paper_name(self, paper_id: str) -> str:
        paper = await self.paper_collection.find_one({"_id": ObjectId(paper_id)})
        return paper["paperType"] if paper else None

    async def get_lamination_name(self, lamination_id: str) -> str:
        lamination = await self.lamination_collection.find_one({"_id": ObjectId(lamination_id)})
        return lamination["laminationType"] if lamination else None

    async def get_customer_name(self, customer_id: str) -> str:
        customer = await self.customer_collection.find_one({"_id": ObjectId(customer_id)})
        return customer["fullName"] if customer else None
    
    async def get_customer(self, customer_id: str) -> str:
        customer = await self.customer_collection.find_one({"_id": ObjectId(customer_id)})
        return customer if customer else None