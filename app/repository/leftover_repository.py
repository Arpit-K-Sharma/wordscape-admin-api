from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId, DBRef
from app.config.db_config import database

class LeftoverRepository:
    def __init__(self):
        self.database = database

    async def create_leftover(self, leftover: dict):
        result = await self.database["leftovers"].insert_one(leftover)
        return str(result.inserted_id)

    async def insert_leftover_items(self, order_id: DBRef, items: list):
        result = await self.database["leftovers"].update_one(
            {"order_id": order_id},
            {"$push": {"items": {"$each": items}}}
        )
        return str(result.modified_count)

    async def find_leftover(self, order_id: DBRef):
        leftover = await self.database["leftovers"].find_one({"order_id": order_id})
        return leftover if leftover else None
    
    async def update_inventory(self, quantity_to_add, item_id, inventory_id):
        inventory = await self.database["inventory"].update_one(
            {
                "_id": ObjectId(inventory_id),
                "item._id": ObjectId(item_id)
            },
            {
                "$set": {"item.$.availability": quantity_to_add}
            }
        )
        return inventory.modified_count

    async def find_inventory(self, item_id: str, inventory_id: str):
        inventory = await self.database["inventory"].find_one(
            {"_id": ObjectId(inventory_id)},
            {"item": {"$elemMatch": {"_id": ObjectId(item_id)}}}
        )
        return inventory

    async def get_all_leftovers(self):
        cursor = self.database["leftovers"].find()
        leftovers = await cursor.to_list(length=None)
        return [self._convert_object_id(leftover) for leftover in leftovers]

    async def get_individual_leftovers(self, order_id: str):
        individual_leftovers = await self.database["leftovers"].find({"order_id.$id": ObjectId(order_id)}).to_list(length=None)
        return [self._convert_object_id(leftover) for leftover in individual_leftovers]

    async def get_leftover(self, leftover_id: ObjectId):
        leftover = await self.database["leftovers"].find_one({"_id": leftover_id})
        return self._convert_object_id(leftover) if leftover else None

    async def update_leftover(self, leftover_id: str, leftover: dict):
        result = await self.database["leftovers"].update_one(
            {"_id": ObjectId(leftover_id)},
            {"$push": {"items": leftover}}
        )
        return result

    def _convert_object_id(self, document):
        if document:
            document["_id"] = str(document["_id"])
            document["order_id"] = str(document["order_id"].id)
            for item in document["items"]:
                item["item_id"] = str(item["item_id"].id)
        return document