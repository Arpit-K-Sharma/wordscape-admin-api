from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db_config import database

class SheetSizeRepository:
    def __init__(self):
        self.collection = database["sheetSize"]

    async def find_all(self) -> list:
        cursor = self.collection.find()
        return await cursor.to_list(length=None)

    async def find_by_id(self, id: str) -> dict:
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def create(self, sheet_size: dict) -> dict:
        result = await self.collection.insert_one(sheet_size)
        return await self.find_by_id(str(result.inserted_id))

    async def update(self, id: str, update_data: dict) -> dict:
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Sheet Size not found or no changes made")
        return await self.find_by_id(id)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
