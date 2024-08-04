from app.dto.leftover_dto import LeftoverDTO, UpdateItemDTO
from app.repository.leftover_repository import LeftoverRepository
from fastapi import Depends, HTTPException
from bson import ObjectId, DBRef

class LeftoverService:
    def __init__(self, repo: LeftoverRepository = Depends()):
        self.repo = repo

    async def create_leftover(self, leftover: LeftoverDTO):
      leftover_dict = leftover.dict()
      order_id = DBRef("orders", ObjectId(leftover_dict["order_id"]))
      leftover_dict["order_id"] = order_id
      
      for item in leftover_dict["items"]: 
        inventory = await self.repo.find_inventory(item["item_id"], item["inventory_id"])
        items_data = inventory["item"][0]
        quantity_to_add = item["quantity"] + items_data["availability"]
        print(quantity_to_add, item["item_id"], item["inventory_id"])
        updated_inventory = await self.repo.update_inventory(quantity_to_add, item["item_id"], item["inventory_id"])
        print(updated_inventory)


      existing_leftover = await self.repo.find_leftover(order_id)

      if existing_leftover is not None:
          for item in leftover_dict["items"]:
              item["item_id"] = DBRef("inventory", ObjectId(item["item_id"]))
          return await self.repo.insert_leftover_items(order_id, leftover_dict["items"])
      else:
          for item in leftover_dict["items"]:
              item["item_id"] = DBRef("inventory", ObjectId(item["item_id"]))
          return await self.repo.create_leftover(leftover_dict)

    async def get_all_leftovers(self):
        return await self.repo.get_all_leftovers()

    async def get_individual_leftovers(self, order_id: str):
        return await self.repo.get_individual_leftovers(order_id)

    async def update_leftover_item(self, leftover_id: str, item: UpdateItemDTO):
        leftover = await self.repo.get_leftover(ObjectId(leftover_id))
        if not leftover:
            raise HTTPException(status_code=404, detail="Leftover not found")

        item = item.dict()
        item["item_id"] = DBRef("inventory", ObjectId(item["item_id"]))
        leftover = await self.repo.update_leftover(leftover_id, item)

        if leftover.modified_count > 0:
            return "successful"
        else:
            return "Couldn't Update it"