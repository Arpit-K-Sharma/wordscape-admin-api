# app/service/paper_thickness_service.py
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from app.repository.paper_thickness_repository import PaperThicknessRepository
from app.dto.paper_thickness_dto import PaperThicknessDTO, PaperThicknessResponseDTO

class PaperThicknessService:
    def __init__(self):
        self.repository = PaperThicknessRepository()

    async def create_paper_thickness(self, paper_thickness_dto: PaperThicknessDTO) -> PaperThicknessResponseDTO:
        paper_thickness_dict = paper_thickness_dto.dict(exclude_unset=True)
        paper_thickness_dict["_id"] = ObjectId()
        result = await self.repository.create(paper_thickness_dict)
        return PaperThicknessResponseDTO(**result)

    async def get_all_paper_thicknesses(self) -> List[PaperThicknessResponseDTO]:
        paper_thicknesses = await self.repository.find_all_sorted()
        return [PaperThicknessResponseDTO(**thickness) for thickness in paper_thicknesses]

    async def get_paper_thickness_by_id(self, thickness_id: str) -> PaperThicknessResponseDTO:
        paper_thickness = await self.repository.find_by_id(thickness_id)
        if not paper_thickness:
            raise HTTPException(status_code=404, detail="Paper Thickness not found")
        return PaperThicknessResponseDTO(**paper_thickness)

    async def update_paper_thickness(self, thickness_id: str, paper_thickness_update: PaperThicknessDTO) -> PaperThicknessResponseDTO:
        existing_paper_thickness = await self.repository.find_by_id(thickness_id)
        if not existing_paper_thickness:
            raise HTTPException(status_code=404, detail="Paper Thickness not found")

        update_data = paper_thickness_update.dict(exclude_unset=True)
        updated_paper_thickness = await self.repository.update(thickness_id, update_data)
        return PaperThicknessResponseDTO(**updated_paper_thickness)

    async def delete_paper_thickness(self, thickness_id: str):
        result = await self.repository.delete(thickness_id)
        if not result:
            raise HTTPException(status_code=404, detail="Paper Thickness not found")