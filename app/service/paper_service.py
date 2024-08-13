from typing import List
from fastapi import HTTPException
from app.repository.paper_repository import PaperRepository
from app.dto.paper_dto import PaperDTO, PaperResponseDTO
from bson import ObjectId

class PaperService:
    def __init__(self):
        self.repository = PaperRepository()

    async def get_all_papers(self) -> List[PaperResponseDTO]:
        paper_items = await self.repository.find_all_papers()
        return [PaperResponseDTO(**item) for item in paper_items]

    async def create_paper(self, paper_dto: PaperDTO) -> PaperResponseDTO:
        paper_dict = paper_dto.dict(exclude_unset=True)
        paper_dict["_id"] = ObjectId()
        result = await self.repository.create_paper(paper_dict)
        if result:
            return PaperResponseDTO(**paper_dict)
        raise HTTPException(status_code=400, detail="Error Adding Paper")

    async def get_paper_by_id(self, paper_id: str) -> PaperResponseDTO:
        paper = await self.repository.find_paper_by_id(paper_id)
        if paper:
            return PaperResponseDTO(**paper)
        raise HTTPException(status_code=404, detail="Paper not found")

    async def update_paper(self, paper_id: str, paper_update: PaperDTO) -> PaperResponseDTO:
        existing_paper = await self.repository.find_paper_by_id(paper_id)
        if not existing_paper:
            raise HTTPException(status_code=404, detail="Paper not found")

        update_data = {k: v for k, v in paper_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return PaperResponseDTO(**existing_paper)

        result = await self.repository.update_paper(paper_id, update_data)
        if result:
            updated_paper = await self.repository.find_paper_by_id(paper_id)
            return PaperResponseDTO(**updated_paper)
        raise HTTPException(status_code=404, detail="Paper not found")

    async def delete_paper(self, paper_id: str):
        result = await self.repository.delete_paper(paper_id)
        if not result:
            raise HTTPException(status_code=404, detail="Paper not found")
        return "Paper Deleted Successfully"
