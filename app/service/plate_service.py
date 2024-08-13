# app/service/plate_service.py
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from app.repository.plate_repository import PlateRepository
from app.dto.plate_dto import PlateDTO, PlateResponseDTO

class PlateService:
    def __init__(self):
        self.repository = PlateRepository()

    async def get_all_plates(self) -> List[PlateResponseDTO]:
        plate_items = await self.repository.find_all_plates()
        return [PlateResponseDTO(**item) for item in plate_items]

    async def create_plate(self, plate_dto: PlateDTO) -> str:
        plate_dict = plate_dto.dict(exclude_unset=True)
        plate_dict["_id"] = ObjectId()
        result = await self.repository.create_plate(plate_dict)
        if result:
            return "Plate Added Successfully"
        raise HTTPException(status_code=400, detail="Error Adding Plate")

    async def update_plate(self, plate_id: str, plate_update: PlateDTO) -> str:
        # Retrieve the existing plate
        existing_plate = await self.repository.find_plate_by_id(plate_id)
        if not existing_plate:
            raise HTTPException(status_code=404, detail="Plate not found")

        # Prepare the update data with only the fields provided
        update_data = {k: v for k, v in plate_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return "No fields provided for update"

        # Update the plate with the prepared data
        result = await self.repository.update_plate(plate_id, update_data)
        if result:
            return "Plate Updated Successfully"
        raise HTTPException(status_code=404, detail="Plate not found")

    async def delete_plate(self, plate_id: str) -> str:
        result = await self.repository.delete_plate(plate_id)
        if not result:
            raise HTTPException(status_code=404, detail="Plate not found")
        return "Plate Deleted Successfully"
