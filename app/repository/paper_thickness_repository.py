# app/repository/paper_thickness_repository.py
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db_config import database

class PaperThicknessRepository:
    def __init__(self):
        self.collection = database["paperThickness"]

    async def create(self, paper_thickness: dict) -> dict:
        result = await self.collection.insert_one(paper_thickness)
        return await self.find_by_id(str(result.inserted_id))

    async def find_all_sorted(self) -> list:
        cursor = self.collection.find().sort("thickness", 1)
        return await cursor.to_list(length=None)

    async def find_by_id(self, thickness_id: str) -> dict:
        return await self.collection.find_one({"_id": ObjectId(thickness_id)})

    async def update(self, thickness_id: str, update_data: dict) -> dict:
        await self.collection.update_one({"_id": ObjectId(thickness_id)}, {"$set": update_data})
        return await self.find_by_id(thickness_id)

    async def delete(self, thickness_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(thickness_id)})
        return result.deleted_count > 0