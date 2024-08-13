from typing import List
from bson import ObjectId
from fastapi import HTTPException
from app.repository.ink_repository import InkRepository
from app.dto.ink_dto import InkDTO, InkResponseDTO

class InkService:
    def __init__(self):
        self.repository = InkRepository()

    async def get_all_inks(self) -> List[InkResponseDTO]:
        ink_items = await self.repository.find_all_inks()
        return [InkResponseDTO(**item) for item in ink_items]

    async def create_ink(self, ink_dto: InkDTO) -> InkResponseDTO:
        ink_dict = ink_dto.dict(exclude_unset=True)
        result = await self.repository.create_ink(ink_dict)
        if result:
            return InkResponseDTO(**ink_dict)
        raise HTTPException(status_code=400, detail="Error Adding Ink")

    async def get_ink_by_id(self, ink_id: str) -> InkResponseDTO:
        ink = await self.repository.find_ink_by_id(ink_id)
        if ink:
            return InkResponseDTO(**ink)
        raise HTTPException(status_code=404, detail="Ink not found")

    async def update_ink(self, ink_id: str, ink_update: InkDTO) -> str:
        # Retrieve the existing ink
        existing_ink = await self.repository.find_ink_by_id(ink_id)
        if not existing_ink:
            raise HTTPException(status_code=404, detail="Ink not found")

        # Prepare the update data with only the fields provided
        update_data = {k: v for k, v in ink_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return "No fields provided for update"

        # Update the ink with the prepared data
        result = await self.repository.update_ink(ink_id, update_data)
        if result:
            return "Ink Updated Successfully"
        raise HTTPException(status_code=404, detail="Ink not found")

    async def delete_ink(self, ink_id: str) -> str:
        result = await self.repository.delete_ink(ink_id)
        if not result:
            raise HTTPException(status_code=404, detail="Ink not found")
        return "Ink Deleted Successfully"

    async def delete_ink(self, ink_id: str) -> str:
        result = await self.repository.delete_ink(ink_id)
        if not result:
            raise HTTPException(status_code=404, detail="Ink not found")
        return "Ink Deleted Successfully"
