# repositories/reorder_repository.py
from app.config.db_config import database
from app.models.purchase_order import PurchaseEntry
from bson import ObjectId, DBRef
from datetime import datetime

class ReorderRepository:

    @staticmethod
    async def insert_reorder(reorder_data: PurchaseEntry, order_id : str):
        reorder_dict = reorder_data.dict(by_alias=True)
        update_result = await database["purchase_orders"].update_one(
            {"orderId": DBRef("orders" , order_id)},
            {"$push": {"purchaseEntry": reorder_dict}}
        )
        update_status = await database["purchase_orders"].update_one(
            {"orderId" : DBRef("orders" , order_id)},
            {"$set": {"isCompleted" : False}}
        )
    # async def find_inventory_from_id(self, itemId: str):
    #    inventory =  await database["inventory"].find_one({"_id": ObjectId(itemId)})
    #    return inventory

    # async def remove_stock_from_inventory(self, itemId: str, quantity: int):
    #     await database["inventory"].update_one(
    #         {"_id": ObjectId(itemId)},{"$set": {"availability": quantity}}
    #     )



