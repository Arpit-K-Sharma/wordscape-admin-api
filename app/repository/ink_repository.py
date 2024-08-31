from typing import List, Dict
from bson import ObjectId
from app.config.db_config import database

class InkRepository:
    def __init__(self):
        self.collection = database["ink"]

    async def find_all_inks(self) -> List[Dict]:
        inks = await self.collection.find().to_list(length=None)
        return inks

    async def create_ink(self, ink_dict: Dict) -> str:
        result = await self.collection.insert_one(ink_dict)
        return str(result.inserted_id)

    async def update_ink(self, ink_id: str, ink_update: Dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(ink_id)},
            {"$set": ink_update}
        )
        return result.modified_count > 0

    async def delete_ink(self, ink_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(ink_id)})
        return result.deleted_count > 0

    async def find_ink_by_id(self, ink_id: str) -> Dict:
        ink = await self.collection.find_one({"_id": ObjectId(ink_id)})
        return ink
