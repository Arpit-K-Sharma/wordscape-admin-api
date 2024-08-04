from fastapi import HTTPException
from app.repository.staff_repo import StaffRepository
from app.dto.staff_dto import StaffDTO, StaffResponseDTO
from app.models.staff import Staff
from app.config.db_config import department_collection
from datetime import date
from app.utils.auth_utils import get_password_hash
from bson import DBRef

class StaffService:
    def __init__(self):
        self.repository = StaffRepository()

    #HELPER FUNCTION
    @staticmethod
    async def get_department_names_from_id(dept_ids):
        # Extract ObjectId from DBRef
        dept_object_ids = [dept_id.id if isinstance(dept_id, DBRef) else dept_id for dept_id in dept_ids]

        # Query the department_collection for matching _ids
        cursor = department_collection.find({"_id": {"$in": dept_object_ids}})
        departments = await cursor.to_list(length=None)

        # Create a list of department names
        department_names = [department["department_name"] for department in departments]

        return department_names
    


    async def add_staff(self, staff_dto: StaffDTO):
        # Convert StaffDTO to Staff, ensuring dept_id is converted to DBRef
        staff_dict = staff_dto.dict(exclude_unset=True)
        staff_dict['password'] = get_password_hash(staff_dict.get('password'))
        staff_dict['created_at'] = date.today()  # Set created_at to current date
        staff = Staff(**staff_dict)
        
        # Insert staff into the repository
        result = await self.repository.insert_staff(staff)
        if result:
            return "Staff Added Successfully"
        raise HTTPException(status_code=404, detail="Error Adding Staff !!!")
    

    async def get_all_staff(self):
        staff_dicts = await self.repository.find_all_staff()
        print(staff_dicts)
        for staff_dict in staff_dicts:
            dept_ids = staff_dict["dept_ids"]
            department_names = await StaffService.get_department_names_from_id(dept_ids)
            staff_dict["departmentNames"] = department_names

        staffs = [StaffResponseDTO(**staff_dict) for staff_dict in staff_dicts]
        return staffs
    

    async def get_staff_by_id(self, staff_id: str):
        staff_dict = await self.repository.find_staff_by_id(staff_id)
        if staff_dict:
            dept_ids = staff_dict["dept_ids"]
            
            department_names = await StaffService.get_department_names_from_id(dept_ids)

            # Add the department names to the staff_dict
            staff_dict["departmentNames"] = department_names
            return StaffResponseDTO(**staff_dict)
        
        raise HTTPException(status_code=404, detail="Staff Not Found !!!")
    

    @staticmethod
    async def get_active_staffs():
        staff_dicts = await StaffRepository.find_active_staffs()
        if staff_dicts:
            return [StaffResponseDTO(**staff_dict) for staff_dict in staff_dicts]
        raise HTTPException(status_code=404, detail="Error Finding Staff !!!")
    

    async def update_staff(self,staff_id: str, staff_dto: StaffDTO):
        staff_dict = staff_dto.dict(exclude_unset=True)
        staff = await self.repository.find_staff_by_id(staff_id)
        created_at = staff["created_at"]
        staff_dict["created_at"] = created_at
        staff = Staff(**staff_dict)

        updated_staff = await self.repository.update_staff(staff_id,staff)
        if updated_staff:
            return "Staff Updated Successfully"
        raise HTTPException(status_code=404, detail="Error Updating Staff !!!")
    

    async def delete_staff(self, staff_id: str):
        response = await self.repository.delete_staff(staff_id)
        if response:
            return "Staff Deleted Successfully"
        raise HTTPException(status_code=404, detail="Error Deleting Staff !!!")
    

    async def deactivate_staff(self,staff_id: str):
        response = await self.repository.deactivate_staff(staff_id)
        if response:
            return "Staff Deactivated"
        raise HTTPException(status_code=404, detail="Error Deacttivating Staff !!!")
    

    async def reactivate_staff(self,staff_id: str):
        response = await self.repository.reactivate_staff(staff_id)
        if response:
            return "Staff Reactivated"
        raise HTTPException(status_code=404, detail="Error Reacttivating Staff !!!")
    

    async def find_staff_by_department_id(self, department_id: str):
        staff_dicts = await self.repository.find_staff_by_department_id(department_id)
        staffs = [StaffResponseDTO(**staff_dict) for staff_dict in staff_dicts]
        return staffs      




