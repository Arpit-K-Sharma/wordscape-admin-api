from app.config.db_config import database
from bson import ObjectId, DBRef
import logging

class PurchaseOrderRepository:

    async def create_purchase_order(self, purchase_order_data: dict):
        new_purchase_order = await database["purchase_orders"].insert_one(purchase_order_data)
        return new_purchase_order.inserted_id
    
    async def change_status(self, purchase_order_id: str):
        result = await database["order"].update_one(
            {"_id": ObjectId(purchase_order_id)},
            {"$set": {"purchase_order_created": True}}
        )
        if result.modified_count > 0:
            return "Successful"
        else:
            return "No document was updated"

    async def update_inventory(self, inventoryId: ObjectId, itemId: ObjectId, new_availability: int):
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

    async def get_inventory_item(self, itemId: ObjectId, inventoryId: ObjectId):
        return  await database["inventory"].find_one(
           {"_id": ObjectId(inventoryId), "item._id": ObjectId(itemId)},
           {"item.$": 1}
        )


    async def insert_inventory_item(self, item: dict):
        await database["inventory"].insert_one(item)

    async def create_purchase_entry(self, purchase_entry_data: dict, purchaseEntryId: ObjectId, order_id: str):  
        result = await database["purchase_orders"].update_one(
            {"orderId": DBRef("orders", order_id), "purchaseEntry._id": ObjectId(purchaseEntryId)},
            {"$set": purchase_entry_data}
        )
        return result.modified_count

    async def update_entry_items(self, order_id: str, item: dict, purchase_entry_objectId: ObjectId, item_update_data: dict):
            order_dbref = DBRef("orders", order_id)
            item_dbref = item["itemId"]
            purchaseEntryId = str(purchase_entry_objectId)
            result = await database["purchase_orders"].update_one(
                {
                    "orderId": order_dbref,
                    "purchaseEntry._id": ObjectId(purchaseEntryId),
                    "purchaseEntry.items.itemId": item_dbref
                },
                {"$set": item_update_data},
                array_filters=[
                    {"entry._id": ObjectId(purchaseEntryId)}, 
                    {"item.itemId": item_dbref}
                ]
            )

    async def update_purchase_order_completion(self, order_id: str, entry_id: ObjectId):
        await database["purchase_orders"].update_one(
            {"orderId": DBRef("orders", order_id), "purchaseEntry._id": ObjectId(entry_id.id)},
            {"$set": {"purchaseEntry.$.isCompleted": True}}
        )

    async def update_whole_purchase_order_completion(self, order_id: str):
        await database["purchase_orders"].update_one(
            {"orderId": DBRef("orders" , order_id)},
            {"$set": {"isCompleted": True}}
        )

    async def get_purchase_entry_by_id(self, purchaseEntryId: str):
        return await database["purchase_orders"].find_one({"orderId": DBRef("orders", purchaseEntryId)})

    async def get_purchase_order_by_id(self, id: ObjectId):
        return await database["purchase_orders"].find_one({"_id": ObjectId(id)})
    
    async def get_purchase_order_by_order_id(self, order_id: str):
        return await database["purchase_orders"].find_one({"orderId": DBRef("orders", order_id)})

    async def update_purchase_order(self, object_data: dict, id:str):
        result = await database["purchase_orders"].update_one(
            {"_id": ObjectId(id)},
            {"$set": object_data}
        )
        return id

    async def get_purchase_orders_without_entries(self):
        print("3")
        cursor = database["purchase_orders"].find({"isCompleted": False})
        return await cursor.to_list(length=None)

    async def get_purchase_orders_with_all_entries(self):
        cursor = database["purchase_orders"].find({"isCompleted": True})
        return await cursor.to_list(length=None)
    
    async def get_reorder_entries(self):
        pipeline = [
            {
                "$match": {
                    "purchaseEntry.tag": "reorder"
                }
            },
            {
                "$project": {
                    "orderId": 1,
                    "isCompleted": 1,
                    "purchaseEntry": {
                        "$filter": {
                            "input": "$purchaseEntry",
                            "as": "entry",
                            "cond": {"$eq": ["$$entry.tag", "reorder"]}
                        }
                    }
                }
            }
        ]
        reorders = await database["purchase_orders"].aggregate(pipeline).to_list(None)
        return reorders