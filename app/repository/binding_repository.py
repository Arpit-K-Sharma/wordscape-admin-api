# app/repository/binding_repository.py
from typing import List, Dict
from bson import ObjectId
from app.config.db_config import database

class BindingRepository:
    def __init__(self):
        self.collection = database["binding"]

    async def find_all_bindings(self) -> List[Dict]:
        bindings = await self.collection.find().to_list(length=None)
        return bindings

    async def create_binding(self, binding_dict: Dict) -> str:
        result = await self.collection.insert_one(binding_dict)
        return str(result.inserted_id)

    async def update_binding(self, binding_id: str, binding_update: Dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(binding_id)},
            {"$set": binding_update}
        )
        return result.modified_count > 0

    async def delete_binding(self, binding_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(binding_id)})
        return result.deleted_count > 0

    async def find_binding_by_id(self, binding_id: str) -> Dict:
        binding = await self.collection.find_one({"_id": ObjectId(binding_id)})
        return binding