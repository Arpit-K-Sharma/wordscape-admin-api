# app/service/paper_size_service.py
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from app.repository.paper_size_repository import PaperSizeRepository
from app.dto.paper_size_dto import PaperSizeDTO, PaperSizeResponseDTO

class PaperSizeService:
    def __init__(self):
        self.repository = PaperSizeRepository()

    async def create_paper_size(self, paper_size_dto: PaperSizeDTO) -> PaperSizeResponseDTO:
        paper_size_dict = paper_size_dto.dict(exclude_unset=True)
        paper_size_dict["_id"] = ObjectId()
        result = await self.repository.create(paper_size_dict)
        return PaperSizeResponseDTO(**result)

    async def get_all_paper_sizes(self) -> List[PaperSizeResponseDTO]:
        paper_sizes = await self.repository.find_all()
        return [PaperSizeResponseDTO(**size) for size in paper_sizes]

    async def get_paper_size_by_id(self, paper_size_id: str) -> PaperSizeResponseDTO:
        paper_size = await self.repository.find_by_id(paper_size_id)
        if not paper_size:
            raise HTTPException(status_code=404, detail="Paper Size not found")
        return PaperSizeResponseDTO(**paper_size)

    async def update_paper_size(self, paper_size_id: str, paper_size_update: PaperSizeDTO) -> PaperSizeResponseDTO:
        existing_paper_size = await self.repository.find_by_id(paper_size_id)
        if not existing_paper_size:
            raise HTTPException(status_code=404, detail="Paper Size not found")

        update_data = {k: v for k, v in paper_size_update.dict().items() if v is not None}
        if not update_data:
            return PaperSizeResponseDTO(**existing_paper_size)

        updated_paper_size = await self.repository.update(paper_size_id, update_data)
        return PaperSizeResponseDTO(**updated_paper_size)

    async def delete_paper_size(self, paper_size_id: str):
        result = await self.repository.delete(paper_size_id)
        if not result:
            raise HTTPException(status_code=404, detail="Paper Size not found")