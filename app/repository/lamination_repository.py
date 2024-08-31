from typing import List, Dict
from bson import ObjectId
from app.config.db_config import database

class LaminationRepository:
    def __init__(self):
        self.collection = database["lamination"]

    async def find_all_laminations(self) -> List[Dict]:
        laminations = await self.collection.find().to_list(length=None)
        return laminations

    async def create_lamination(self, lamination_dict: Dict) -> str:
        result = await self.collection.insert_one(lamination_dict)
        return str(result.inserted_id)

    async def update_lamination(self, lamination_id: str, lamination_update: Dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(lamination_id)},
            {"$set": lamination_update}
        )
        return result.modified_count > 0

    async def delete_lamination(self, lamination_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(lamination_id)})
        return result.deleted_count > 0

    async def find_lamination_by_id(self, lamination_id: str) -> Dict:
        lamination = await self.collection.find_one({"_id": ObjectId(lamination_id)})
        return lamination
