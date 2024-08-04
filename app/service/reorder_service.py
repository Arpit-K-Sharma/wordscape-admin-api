# services/reorder_service.py
from app.models.purchase_order import PurchaseEntry
from app.repository.reorder_repository import ReorderRepository

class ReorderService:
    def __init__(self):
        self.repository = ReorderRepository()

    async def create_reorder(self, reorder_data: PurchaseEntry, order_id: str):
        try:
            await self.repository.insert_reorder(reorder_data, order_id)
            reorder_data = reorder_data.dict()
            # for item in reorder_data["items"]:
                
            #     itemId = item["itemId"].id
            #     quantity = item["quantityFromVendor"]
            #     inventory = await self.repository.find_inventory_from_id(itemId)
            #     quantity_of_inventory = inventory["availability"]
            #     new_quantity = quantity_of_inventory - quantity
            #     await self.repository.remove_stock_from_inventory(itemId, new_quantity)

        except Exception as e:
            return False, str(e)
