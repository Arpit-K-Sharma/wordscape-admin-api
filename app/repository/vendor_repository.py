# repositories/vendor_repository.py
from app.config.db_config import database
from app.models.vendors_model import Vendor
from app.dto.vendor_dto import VendorDTO
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

class VendorRepository:

    async def insert_vendor(self, vendor_data: dict):
        result = await database["vendors"].insert_one(vendor_data)
        return result.inserted_id

    async def find_vendor_by_id(self, vendorId: str):
        vendor_object = await database["vendors"].find_one({"_id": ObjectId(vendorId)})
        return VendorDTO(**vendor_object)

    async def find_all_vendors(self):
        return await database["vendors"].find().to_list(length=None)

    async def update_vendor(self, vendorId: str, update_data: dict):
        await database["vendors"].update_one(
            {"_id": ObjectId(vendorId)},
            {"$set": update_data}
        )
        return await self.find_vendor_by_id(vendorId)

    async def delete_vendor(self, vendorId: str):
        result = await database["vendors"].delete_one({"_id": ObjectId(vendorId)})
        return result.deleted_count
