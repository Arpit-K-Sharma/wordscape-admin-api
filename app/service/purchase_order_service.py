from fastapi import HTTPException
from app.models.purchase_order import PurchaseOrder
from app.repository.purchase_order_repository import PurchaseOrderRepository
from app.models.purchase_entry import PurchaseEntry
from bson import ObjectId

class PurchaseOrderService:
    def __init__(self, repo: PurchaseOrderRepository):
        self.repo = repo

    async def create_purchase_order(self, purchase_order_data: PurchaseOrder):
        try:
            purchase_order_data_dict = purchase_order_data.dict(by_alias=True)
            purchase_order_id = await self.repo.create_purchase_order(purchase_order_data_dict)
            await self.repo.change_status(purchase_order_data_dict["orderId"].id)
            await self._remove_item_inventory(purchase_order_id)
            return purchase_order_id
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_purchase_order_by_id(self, order_id: str):
        try:
            return await self.repo.get_purchase_order_by_order_id(order_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    


    async def update_purchase_order(self, update_data: dict, id:str):
        try:
            object_data = PurchaseOrder(**update_data)
            object_data = object_data.dict()
            if "id" in object_data:
              object_data["_id"] = ObjectId(id)
            del object_data["id"] 
            update_purchase_order = await self.repo.update_purchase_order(object_data, id)
            if update_purchase_order is None:
                raise HTTPException(status_code=404, detail="Purchase order not found")
            return await self.repo.get_purchase_order_by_id(update_purchase_order)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_purchase_orders_without_entries(self):
        try:
            print("2")
            return await self.repo.get_purchase_orders_without_entries()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_purchase_orders_with_entries(self):
        try:
            return await self.repo.get_purchase_orders_with_all_entries()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_purchase_entry(self, purchase_entry_data: PurchaseEntry, order_id: str):
        try:
            purchase_entry_dict = purchase_entry_data.dict(by_alias=True)
            update_data = {
        "purchaseEntry.$.image": purchase_entry_dict["image"],
        "purchaseEntry.$.discount": purchase_entry_dict["discount"],
        "purchaseEntry.$.vat": purchase_entry_dict["vat"],
        "purchaseEntry.$.grandTotal": purchase_entry_dict["grandTotal"],
        "purchaseEntry.$.invoiceNo": purchase_entry_dict["invoiceNo"],
        "purchaseEntry.$.invoiceDate": purchase_entry_dict["invoiceDate"]
            }
            
            print("this is" , purchase_entry_dict["purchaseEntryId"].id)
              
            modified_count = await self.repo.create_purchase_entry(update_data, purchase_entry_dict["purchaseEntryId"].id, order_id)
            if modified_count == 0:
                raise HTTPException(status_code=404, detail="Purchase entry not found")
            
            for item in purchase_entry_dict["items"]:
              item_update_data = {
                "purchaseEntry.$[entry].items.$[item].itemCode": item.get("code"),
                "purchaseEntry.$[entry].items.$[item].rate": item.get("rate"),
                "purchaseEntry.$[entry].items.$[item].amount": item.get("amount")
              }
              purchaseEntryId = purchase_entry_dict["purchaseEntryId"].id
              await self.repo.update_entry_items(order_id, item, purchaseEntryId, item_update_data)

            await self._update_inventory(purchase_entry_dict["items"])
            await self._update_vendor_completion(order_id, purchase_entry_dict["purchaseEntryId"])
            await self._update_purchase_order_completion(order_id)
            return "Purchase Entry Created"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def _remove_item_inventory(self, purchase_order_id: str):
        purchase_order = await self.repo.get_purchase_order_by_id(purchase_order_id)
        purchase_entries = purchase_order["purchaseEntry"]
        for entry in purchase_entries:
            items = entry["items"]
            for item in items:
                if item["quantityFromStock"] > 0:
                    itemId = item["itemId"].id
                    inventoryId = item["inventoryId"].id
                    inventory_item = await self.repo.get_inventory_item(itemId, inventoryId)
                    if inventory_item:
                        inventory_items = inventory_item["item"][0]
                        new_availability = inventory_items["availability"] - item["quantityFromStock"]
                        await self.repo.update_inventory(inventoryId, itemId, new_availability)


    async def _update_inventory(self, items: list): 
          for item in items:
            inventory_item = await self.repo.get_inventory_item(item["itemId"].id, item["inventoryId"].id)
            if inventory_item:
                inventory_items = inventory_item["item"][0]
                new_availability = inventory_items["availability"] + item["quantity"]
                itemId = item["itemId"].id
                inventoryId = item["inventoryId"].id
                print(itemId)
                await self.repo.update_inventory(inventoryId, itemId, new_availability)
            else:
                new_inventory_item = {
                    "_id": item["inventoryId"].id,
                    "item": [{
                        "_id": item["itemId"].id,
                        "availability": item["quantity"]
                    }]
                    
                }
                await self.repo.insert_inventory_item(new_inventory_item)

    async def _update_vendor_completion(self, order_id: str, purchaseEntryId: str):
        await self.repo.update_purchase_order_completion(order_id, purchaseEntryId)

    async def _update_purchase_order_completion(self, order_id: str):
        purchase_order = await self.repo.get_purchase_entry_by_id(order_id)
        if not purchase_order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        
        all_completed = all(entry["isCompleted"] for entry in purchase_order["purchaseEntry"])
        if all_completed:
           print("this is ", order_id)
           print("i am trying")
           await self.repo.update_whole_purchase_order_completion(order_id)

    async def get_reorder_entries(self):
        reorder_documents = await self.repo.get_reorder_entries()
        print("ok")
        return [PurchaseOrder(**doc) for doc in reorder_documents]
    
        
