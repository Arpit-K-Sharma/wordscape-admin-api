from bson import ObjectId
from app.dto.department_dto import DepartmentDTO
from app.config.db_config import department_collection

class DepartmentRepository:

    async def insert_department(self, department:DepartmentDTO):
        department_dict = department.dict(exclude_unset=True)
        result = await department_collection.insert_one(department_dict)
        return department_dict

    async def find_department_by_id(self, department_id:str):
        return await department_collection.find_one({"_id":ObjectId(department_id)})
    
    async def find_department_by_name(self, department_name:str):
        return await department_collection.find_one({"department_name": department_name})
    
    async def find_all_departments(self):
        return await department_collection.find().to_list(length = None)
    
    async def update_department(self, department_id:str, updated_department: DepartmentDTO):
        return await department_collection.update_one({"_id":ObjectId(department_id)}, {"$set": updated_department.dict(exclude_unset=True)})

    async def delete_department(self, department_id:str):
        return await department_collection.delete_one({"_id":ObjectId(department_id)})