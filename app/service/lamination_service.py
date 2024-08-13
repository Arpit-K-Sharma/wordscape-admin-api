from typing import List
from fastapi import HTTPException
from app.repository.lamination_repository import LaminationRepository
from app.dto.lamination_dto import LaminationDTO, LaminationResponseDTO

class LaminationService:
    def __init__(self):
        self.repository = LaminationRepository()

    async def get_all_laminations(self) -> List[LaminationResponseDTO]:
        lamination_items = await self.repository.find_all_laminations()
        return [LaminationResponseDTO(**item) for item in lamination_items]

    async def create_lamination(self, lamination_dto: LaminationDTO) -> LaminationResponseDTO:
        lamination_dict = lamination_dto.dict(exclude_unset=True)
        result = await self.repository.create_lamination(lamination_dict)
        if result:
            return LaminationResponseDTO(**lamination_dict)
        raise HTTPException(status_code=400, detail="Error Adding Lamination")

    async def get_lamination_by_id(self, lamination_id: str) -> LaminationResponseDTO:
        lamination = await self.repository.find_lamination_by_id(lamination_id)
        if lamination:
            return LaminationResponseDTO(**lamination)
        raise HTTPException(status_code=404, detail="Lamination not found")

    async def update_lamination(self, lamination_id: str, lamination_update: LaminationDTO) -> str:
        # Retrieve the existing lamination
        existing_lamination = await self.repository.find_lamination_by_id(lamination_id)
        if not existing_lamination:
            raise HTTPException(status_code=404, detail="Lamination not found")

        # Prepare the update data with only the fields provided
        update_data = {k: v for k, v in lamination_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return "No fields provided for update"

        # Update the lamination with the prepared data
        result = await self.repository.update_lamination(lamination_id, update_data)
        if result:
            return "Lamination Updated Successfully"
        raise HTTPException(status_code=404, detail="Lamination not found")

    async def delete_lamination(self, lamination_id: str):
        result = await self.repository.delete_lamination(lamination_id)
        if not result:
            raise HTTPException(status_code=404, detail="Lamination not found")
        return "Lamination Deleted Successfully"
