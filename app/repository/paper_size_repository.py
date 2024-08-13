# app/repository/paper_size_repository.py
from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db_config import database_erp

class PaperSizeRepository:
    def __init__(self):
        self.collection = database_erp["paperSize"]

    async def create(self, paper_size: dict) -> dict:
        result = await self.collection.insert_one(paper_size)
        return await self.find_by_id(str(result.inserted_id))

    async def find_all(self) -> list:
        cursor = self.collection.find()
        return await cursor.to_list(length=None)

    async def find_by_id(self, paper_size_id: str) -> dict:
        return await self.collection.find_one({"_id": ObjectId(paper_size_id)})

    async def update(self, paper_size_id: str, update_data: dict) -> dict:
        result = await self.collection.update_one(
            {"_id": ObjectId(paper_size_id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Paper Size not found or no changes made")
        return await self.find_by_id(paper_size_id)

    async def delete(self, paper_size_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(paper_size_id)})
        return result.deleted_count > 0