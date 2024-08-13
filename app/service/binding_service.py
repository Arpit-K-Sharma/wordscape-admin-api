# app/service/binding_service.py
from typing import List
from fastapi import HTTPException
from app.repository.binding_repository import BindingRepository
from app.dto.binding_dto import BindingDTO, BindingResponseDTO

class BindingService:
    def __init__(self):
        self.repository = BindingRepository()

    async def get_all_bindings(self) -> List[BindingResponseDTO]:
        binding_items = await self.repository.find_all_bindings()
        return [BindingResponseDTO(**item) for item in binding_items]

    async def create_binding(self, binding_dto: BindingDTO):
        binding_dict = binding_dto.dict(exclude_unset=True)
        result = await self.repository.create_binding(binding_dict)
        if result:
            return "Binding Added Successfully"
        raise HTTPException(status_code=400, detail="Error Adding Binding")

    async def update_binding(self, binding_id: str, binding_update: BindingDTO) -> str:
        # Retrieve the existing binding
        existing_binding = await self.repository.find_binding_by_id(binding_id)
        if not existing_binding:
            raise HTTPException(status_code=404, detail="Binding not found")

        # Prepare the update data with only the fields provided
        update_data = {k: v for k, v in binding_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return "No fields provided for update"

        # Update the binding with the prepared data
        result = await self.repository.update_binding(binding_id, update_data)
        if result:
            return "Binding Updated Successfully"
        raise HTTPException(status_code=404, detail="Binding not found")

    async def delete_binding(self, binding_id: str):
        result = await self.repository.delete_binding(binding_id)
        if not result:
            raise HTTPException(status_code=404, detail="Binding not found")
        return "Binding Deleted Successfully"

    async def get_binding_by_id(self, binding_id: str) -> BindingResponseDTO:
        binding = await self.repository.find_binding_by_id(binding_id)
        if not binding:
            raise HTTPException(status_code=404, detail="Binding not found")
        return BindingResponseDTO(**binding)