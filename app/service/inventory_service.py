from app.models.inventory import InventoryItem, Items
from app.repository.inventory_repository import InventoryRepository
from app.models.issued_item import IssuedItem
from typing import List 
from app.dto.inventory_dto import ItemDTO
from app.utils.response_util import get_response
from fastapi import HTTPException
from bson import ObjectId

class InventoryService:
    def __init__(self):
        self.repository = InventoryRepository()

    async def create_inventory_item(self, inventory_data: InventoryItem):
        itemId = await self.repository.insert_inventory_item(inventory_data)
        inventory = await self.repository.find_inventory_item_by_id(str(itemId))
        if inventory:
            return "Inventory Added Successfully"

    async def get_inventory_item_by_id(self, itemId: str):
        return await self.repository.find_inventory_item_by_id(itemId)

    async def get_all_inventory_items(self):
        return await self.repository.find_all_inventory_items()
    
    async def create_issued_item(self, issued: IssuedItem):
        order_id = issued.order_id
        await self._remove_items_from_inventory(order_id)
        issued_item = await self.repository.find_issued_item_by_order_id(order_id)
        if issued_item:
            return "Item Issued Sucessfully"
        else:
            return "Failed to Issue Item"

    async def _remove_items_from_inventory(self, order_id: str):
        purchase_order = await self.repository.find_purchase_order_by_order_id(order_id)
        if not purchase_order:
            raise ValueError(f"Purchase order with orderId {order_id} not found")

        for purchaseEntry in purchase_order["purchaseEntry"]:
                if purchaseEntry.get("is_issued") is not None or purchaseEntry.get("isCompleted") is False:
                    None
                else:
                    entry_id = purchaseEntry["_id"]
                    await self.repository.update_status_of_order(order_id, entry_id)
    
                    for item in purchaseEntry["items"]:
                      itemId = item["itemId"].id
                      inventoryId = item["inventoryId"].id
                      quantity_to_remove = item["quantityFromVendor"]
                      inventory_item = await self.repository.find_inventory_item_by_id(inventoryId)
                      if inventory_item:
                          inventory_items = inventory_item["item"]
                          for item in inventory_items:
                              if item["_id"] == ObjectId(itemId):
                                new_availability = item["availability"] - quantity_to_remove
                                if new_availability < 0:
                                  raise ValueError(f"Not enough inventory for item {itemId}")
                                await self.repository.update_inventory_item(inventoryId, itemId, new_availability)
                      else:
                          raise ValueError(f"Inventory item with itemId {itemId} not found")
                      
    async def update_availability(self, inventoryId: str, itemId: str, new_availability: int):
        inventory_item = await self.repository.find_inventory_item_by_id(inventoryId)
        if inventory_item:
            update_item = next((item for item in inventory_item["item"] if str(item["_id"]) == itemId), None)
        if update_item:
            update_item["availability"] = new_availability
            await self.repository.update_availability(inventoryId, itemId, new_availability)
        return str(inventory_item["_id"])


    async def add_itemType(self, inventoryId: str, items: List[ItemDTO]):
        new_items = []
        for item in items:
            item_data_dict = item.dict(exclude_none=True)
            created_item = Items(**item_data_dict)
            new_items.append(created_item)
        await self.repository.add_typeItem(inventoryId, new_items)
        return len(new_items)
    
    async def delete_type(self, itemId: str):
        try:
            delete_count = await self.repository.delete_type(itemId)
            if delete_count:
                return get_response(status="success", message="Item type deleted successfully", status_code=200)
            else:
                raise HTTPException(status_code=404, detail="Vendor not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        
    async def delete_item(self, inventoryId:str, itemId: str):
        try:
            delete_count = await self.repository.delete_item(inventoryId, itemId)
            if delete_count:
                return get_response(status="success", message="Item type deleted successfully", status_code=200)
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    
            
            
    
        
            

