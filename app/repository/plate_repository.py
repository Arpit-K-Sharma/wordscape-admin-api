# app/repository/plate_repository.py
from typing import List, Dict
from bson import ObjectId
from app.config.db_config import database_erp

class PlateRepository:
    def __init__(self):
        self.collection = database_erp["plate"]

    async def find_all_plates(self) -> List[Dict]:
        plates = await self.collection.find().to_list(length=None)
        return plates

    async def create_plate(self, plate_dict: Dict) -> str:
        result = await self.collection.insert_one(plate_dict)
        return str(result.inserted_id)

    async def update_plate(self, plate_id: str, plate_update: Dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(plate_id)},
            {"$set": plate_update}
        )
        return result.modified_count > 0

    async def delete_plate(self, plate_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(plate_id)})
        return result.deleted_count > 0

    async def find_plate_by_id(self, plate_id: str) -> Dict:
        plate = await self.collection.find_one({"_id": ObjectId(plate_id)})
        return plate
