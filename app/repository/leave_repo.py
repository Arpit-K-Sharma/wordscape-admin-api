from bson import DBRef, ObjectId
from app.config.db_config import leave_collection
from app.models.leave import Leave
from datetime import date, datetime

class LeaveRepository:

    async def insert_leave(self, leave: Leave):
        leave_dict = leave.dict(exclude_unset=True)
        result = await leave_collection.insert_one(leave_dict)
        return leave_dict

    async def find_all_leaves(self):
        cursor = leave_collection.find()
        return await cursor.to_list(length=None)

    async def update_leave(self, leave_id: str, leave_update: Leave):
        return await leave_collection.update_one({"_id": ObjectId(leave_id)}, {"$set": leave_update.dict(exclude_unset=True)})

    async def update_leave_status(self, leave_id: str, status: str):
        return await leave_collection.update_one({"_id": ObjectId(leave_id)}, {"$set": {"status": status}})
    
    @staticmethod
    async def find_leave_record_for_date(date: date):
        query_date = datetime.strptime(date, "%d-%m-%Y")   

        leaves = await leave_collection.find({
            "start_date": {"$lte": query_date},
            "end_date": {"$gte": query_date},
            "status": "Approved"
        }).to_list(length=None)  

        return leaves
    
    @staticmethod
    async def get_leave_by_staff_id(staff_id:str):  
        staff_dbref = DBRef("staff",ObjectId(staff_id))      
        leaves = await leave_collection.find({"staff_id":staff_dbref}).to_list(length=None)
        return leaves


    
