from fastapi import HTTPException
from app.repository.department_repo import DepartmentRepository
from app.dto.department_dto import DepartmentDTO

class DepartmentService:
    def __init__(self):
        self.repository = DepartmentRepository()

    async def add_department(self, department: DepartmentDTO):
        department_dict = await self.repository.insert_department(department)
        if department_dict:
            return "Department Added Successfully"
        raise HTTPException(status_code= 404, detail= "Error Adding Department !!!")
    
    async def update_department(self, department_id:str, department:DepartmentDTO):
        updated_department = await self.repository.update_department(department_id, department)
        if updated_department:
            return "Department Updated Successfully"
        raise HTTPException(status_code= 404, detail= "Error Updating Department !!!")
    
    async def get_all_departments(self):
        department_dicts = await self.repository.find_all_departments()
        departments = [DepartmentDTO(**dept_dict) for dept_dict in department_dicts]
        return departments
    
    async def get_by_department_name(self,department_name:str):
        department_dict = await self.repository.find_department_by_name(department_name)
        if department_dict:
            return DepartmentDTO(**department_dict)
        raise HTTPException(status_code= 404, detail= "Department not Found !!!")

    async def get_by_department_id(self,department_id:str):
        department_dict = await self.repository.find_department_by_id(department_id)
        return DepartmentDTO(**department_dict)
    
    async def delete_department(self, department_id:str):
        response = await self.repository.delete_department(department_id)
        if response:
            return "Department Deleted Successfully"
        raise HTTPException(status_code= 404, detail= "Error Deleting Department !!!")


