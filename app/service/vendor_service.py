from app.models.vendors_model import Vendor
from app.repository.vendor_repository import VendorRepository
from app.dto.vendor_dto import VendorDTO
from fastapi import HTTPException
from app.utils.response_util import get_response

class VendorService:
    def __init__(self):
        self.repository = VendorRepository()

    async def create_vendor(self, vendor_data: VendorDTO):
        try:
            
            vendorId = await self.repository.insert_vendor(vendor_data.dict(by_alias=True, exclude_none=True))
            created_vendor = await self.repository.find_vendor_by_id(vendorId)
            if created_vendor:
                return get_response(status="success", message="Vendor Created Sucessfully", status_code=201)
            else:
                raise HTTPException(status_code=500, detail="Vendor could not be created")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_vendor_by_id(self, vendorId: str):
        try:
            vendor = await self.repository.find_vendor_by_id(vendorId)  
            print(vendor)     
            if vendor:
              return get_response(status="success", data=vendor.dict(), status_code=200)
            else:
              raise HTTPException(status_code=404, detail="Vendor not found")
    
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    async def get_all_vendors(self):
        try:
            vendors = await self.repository.find_all_vendors()
            return get_response(status="success", data=[VendorDTO(**vendor).dict(by_alias=True) for vendor in vendors], status_code=200)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def update_vendor(self, vendorId: str, vendor_data: VendorDTO):
        try:
            update_data = vendor_data.dict(exclude_unset=True)
            updated_vendor = await self.repository.update_vendor(vendorId, update_data)
            if updated_vendor:
                return get_response(status="success", message="Vendor Updated Sucessfully", status_code=200)
            else:
                raise HTTPException(status_code=404, detail="Vendor not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_vendor(self, vendorId: str):
        try:
            delete_count = await self.repository.delete_vendor(vendorId)
            if delete_count:
                return get_response(status="success", message="Vendor deleted successfully", status_code=200)
            else:
                raise HTTPException(status_code=404, detail="Vendor not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
