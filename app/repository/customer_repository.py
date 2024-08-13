# app/repository/customer_repository.py
from typing import List, Dict, Tuple
from bson import ObjectId
from app.config.db_config import database_erp

class CustomerRepository:
    def __init__(self):
        self.collection = database_erp["user"]

    async def find_all_customers(self, skip: int, limit: int, sort_field: str, sort_direction: str) -> Tuple[List[dict], int]:
        sort_order = 1 if sort_direction == "asc" else -1
        cursor = self.collection.find({"role":"ROLE_CUSTOMER"}).sort(sort_field, sort_order).skip(skip).limit(limit)
        customers = await cursor.to_list(length=limit)
        total_elements = await self.collection.count_documents({"role":"ROLE_CUSTOMER"})
        return customers, total_elements

    async def find_customer_by_id(self, customer_id: str) -> Dict:
        customer = await self.collection.find_one({"_id": ObjectId(customer_id)})
        return customer

    async def update_customer(self, customer_id: str, customer_update: Dict) -> Dict:
        result = await self.collection.update_one(
            {"_id": ObjectId(customer_id)},
            {"$set": customer_update}
        )
        if result.modified_count > 0:
            return await self.find_customer_by_id(customer_id)
        return None