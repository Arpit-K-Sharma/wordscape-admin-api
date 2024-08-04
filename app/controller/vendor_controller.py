from fastapi import APIRouter, Depends
from app.service.vendor_service import VendorService
from app.dto.vendor_dto import VendorDTO
from app.utils.auth_utils import admin_verification

vendor_route = APIRouter()
vendor_service = VendorService()

@vendor_route.post("/vendor", response_model=VendorDTO, dependencies=[Depends(admin_verification)])
async def create_vendor(vendor_data: VendorDTO):
    return await vendor_service.create_vendor(vendor_data)

@vendor_route.get("/vendor/{vendorId}", response_model=VendorDTO, dependencies=[Depends(admin_verification)])
async def get_vendor(vendorId: str):
    vendor = await vendor_service.get_vendor_by_id(vendorId)
    return vendor

@vendor_route.get("/vendors", response_model=list[VendorDTO], dependencies=[Depends(admin_verification)])
async def get_all_vendors():
    return await vendor_service.get_all_vendors()

@vendor_route.put("/vendor/{vendorId}", response_model=VendorDTO, dependencies=[Depends(admin_verification)])
async def update_vendor(vendorId: str, vendor_data: VendorDTO):
    return await vendor_service.update_vendor(vendorId, vendor_data)

@vendor_route.delete("/vendor/{vendorId}", dependencies=[Depends(admin_verification)])
async def delete_vendor(vendorId: str):
    return await vendor_service.delete_vendor(vendorId)
