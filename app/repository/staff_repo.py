from bson import ObjectId, DBRef
from app.dto.staff_dto import StaffDTO
from app.config.db_config import staff_collection
from app.models.staff import Staff

class StaffRepository:

    async def insert_staff(self, staff: Staff):
        staff_dict = staff.dict(exclude_unset=True)
        result = await staff_collection.insert_one(staff_dict)
        return staff_dict

    async def find_staff_by_id(self, staff_id: str):
        return await staff_collection.find_one({"_id": ObjectId(staff_id)})

    async def find_staff_by_name(self, name: str):
        return await staff_collection.find_one({"fullName": name})
    
    @staticmethod
    async def find_staff_by_email(email: str):
        return await staff_collection.find_one({"email": email})
    
    async def find_all_staff(self):
        cursor = staff_collection.find({"role": "ROLE_USER"})
        return await cursor.to_list(length=None)
    
    async def update_staff(self, staff_id: str, updated_staff: Staff):
        return await staff_collection.update_one({"_id": ObjectId(staff_id)}, {"$set": updated_staff.dict(exclude_unset=True)})

    async def delete_staff(self, staff_id: str):    
        return await staff_collection.delete_one({"_id": ObjectId(staff_id)})

    async def find_staff_by_department_id(self, department_id: str):
        department_dbref = DBRef("department", ObjectId(department_id))
        staff_list = await staff_collection.find({"dept_ids": department_dbref}).to_list(length=None)
        return staff_list
    
    @staticmethod
    async def find_active_staffs():
        return await staff_collection.find({"role":"ROLE_USER","status":True}).to_list(length=None)
    
    async def deactivate_staff(self,staff_id:str):
        return await staff_collection.update_one({"_id":ObjectId(staff_id)},{"$set":{"status":False}})
    
    async def reactivate_staff(self,staff_id:str):
        return await staff_collection.update_one({"_id":ObjectId(staff_id)},{"$set":{"status":True}})
