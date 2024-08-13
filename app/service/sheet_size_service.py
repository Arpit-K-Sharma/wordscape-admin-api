from typing import List, Optional
from fastapi import HTTPException
from app.repository.sheet_size_repository import SheetSizeRepository
from app.dto.sheet_size_dto import SheetSizeDTO, SheetSizeResponseDTO

class SheetSizeService:
    def __init__(self):
        self.repository = SheetSizeRepository()

    async def get_all_sheet_sizes(self) -> List[SheetSizeResponseDTO]:
        sheet_sizes = await self.repository.find_all()
        return [SheetSizeResponseDTO(**size) for size in sheet_sizes]

    async def get_sheet_size_by_id(self, id: str) -> Optional[SheetSizeResponseDTO]:
        sheet_size = await self.repository.find_by_id(id)
        if not sheet_size:
            raise HTTPException(status_code=404, detail="Sheet Size not found")
        return SheetSizeResponseDTO(**sheet_size)

    async def create_sheet_size(self, sheet_size_dto: SheetSizeDTO) -> str:
        sheet_size_dict = sheet_size_dto.dict(exclude_unset=True)
        result = await self.repository.create(sheet_size_dict)
        if result:
            return "Sheet Size Created Successfully"
        raise HTTPException(status_code=400, detail="Error Creating Sheet Size")

    async def update_sheet_size(self, id: str, sheet_size_update: SheetSizeDTO) -> str:
        existing_sheet_size = await self.repository.find_by_id(id)
        if not existing_sheet_size:
            raise HTTPException(status_code=404, detail="Sheet Size not found")

        update_data = {k: v for k, v in sheet_size_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return "No fields provided for update"

        result = await self.repository.update(id, update_data)
        if result:
            return "Sheet Size Updated Successfully"
        raise HTTPException(status_code=404, detail="Sheet Size not found")

    async def delete_sheet_size(self, id: str) -> bool:
        result = await self.repository.delete(id)
        if not result:
            raise HTTPException(status_code=404, detail="Sheet Size not found")
        return True
