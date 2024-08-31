from app.config.db_config import database
from app.models.inventory import InventoryItem, Items
from app.models.issued_item import IssuedItem
from fastapi.encoders import jsonable_encoder
from bson import ObjectId, DBRef
from typing import List
from app.utils.response_util import get_response
from fastapi import HTTPException

class InventoryRepository:

    async def insert_inventory_item(self, inventory_data: InventoryItem):
        inventory_dict = inventory_data.dict(by_alias=True, exclude_none=True)
        database_object = await database["inventory"].insert_one(inventory_dict)
        return database_object.inserted_id

    async def find_inventory_item_by_id(self, itemId: str):
        return await database["inventory"].find_one({"_id": ObjectId(itemId)})

    async def find_all_inventory_items(self):
        return await database["inventory"].find().to_list(length=None)

    async def update_purchase_order(self, order_id: str, issued_data: dict):
        await database["purchase_orders"].update_one({"orderId": order_id}, {"$set": issued_data})

    async def find_purchase_order_by_order_id(self, order_id: str):
        return await database["purchase_orders"].find_one({"orderId": DBRef("orders", order_id)})
    
    async def update_status_of_order(self, order_id: str, entry_id: str): 
        await database["purchase_orders"].update_one(
        {"orderId": DBRef("orders", order_id), "purchaseEntry._id": ObjectId(entry_id)},
        {"$set": {"purchaseEntry.$.is_issued": True}}
    )

    async def update_inventory_item(self, inventoryId: ObjectId, itemId: ObjectId, new_availability: int):
        result = await database["inventory"].find_one_and_update(
           {
            "_id": ObjectId(inventoryId),
            "item._id": ObjectId(itemId)
           },
           {
            "$set": {"item.$.availability": new_availability}
           },
            return_document=True
        )
        return result

    async def find_issued_item_by_order_id(self, itemId: str):
        return await database["purchase_orders"].find_one({"orderId": DBRef("orders" , itemId)})

    async def delete_type(self, itemId: str):
        item_id = ObjectId(itemId)

        result = await database["inventory"].delete_one({"_id": ObjectId(itemId)})
        return result.deleted_count
    
    async def update_availability(self, inventoryId:str, itemId: str, new_availability:str):
        result = await database["inventory"].find_one_and_update(
           {
            "_id": ObjectId(inventoryId),
            "item._id": ObjectId(itemId)
           },
           {
            "$set": {"item.$.availability": new_availability}
           },
            return_document=True
        )
        return result
        
        
    async def add_typeItem(self, inventoryId: str, added_items: List[Items]):
        created_items_dict = [item.dict(by_alias=True, exclude_none=True) for item  in added_items]
        # created_items = [Items(**item_data) for item_data in created_items_dict]
        result = await database["inventory"].update_one(
            {"_id": ObjectId(inventoryId)}, 
            {"$push": {"item": {"$each": created_items_dict}}}
        )
        return result.modified_count
        
    async def delete_item(self, inventoryId: str, itemId: str):
        item_type = await database["inventory"].find_one({"_id": ObjectId(inventoryId)})
        result = await database["inventory"].update_one(
        {"_id": ObjectId(inventoryId)}, 
        {"$pull": {"item": {"_id": ObjectId(itemId)}}}
        )

        if result.modified_count > 0:
            print("Item successfully deleted.")
        else:
            print("No item found with the provided ID.")
        
        return "successful"
    
    ################################### ERP MIGRATION CODE ####################################################
    
    async def find_items_by_type(self, item_type: str):
        inventory_item = await database["inventory"].find_one({"type": item_type})
        return inventory_item['item'] if inventory_item else []

    async def add_item_to_type(self, item_type: str, new_item: dict):
        result = await database["inventory"].update_one(
            {"type": item_type},
            {"$push": {"item": new_item}},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None

    async def update_item_in_type(self, item_type: str, updated_item: dict):
        item_id = updated_item.pop("_id")  # Remove and store the ID
        
        # Prepare the update operation
        update_fields = {}
        for key, value in updated_item.items():
            update_fields[f"item.$.{key}"] = value

        # Perform the update only for provided fields
        result = await database["inventory"].update_one(
            {"type": item_type, "item._id": ObjectId(item_id)},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    async def remove_item_from_type(self, item_type: str, item_id: str):
        result = await database["inventory"].update_one(
            {"type": item_type},
            {"$pull": {"item": {"_id": ObjectId(item_id)}}}
        )
        return result.modified_count > 0
        