# app/service/leave_service.py
from typing import List
from fastapi import HTTPException
from app.repository.leave_repo import LeaveRepository
from app.dto.leave_dto import LeaveDTO, LeaveResponseDTO
from app.config.db_config import staff_collection
from app.models.leave import Leave
from datetime import datetime, date
from bson import ObjectId, DBRef

class LeaveService:
    def __init__(self):
        self.repository = LeaveRepository()

    #HELPER METHOD
    @staticmethod
    async def get_staff_name_from_dbref(staff_dbref: DBRef) -> str:
        staff_id = staff_dbref.id if isinstance(staff_dbref, DBRef) else staff_dbref
        staff_doc = await staff_collection.find_one({"_id": ObjectId(staff_id)})
        return staff_doc["fullName"] if staff_doc else None


    async def add_leave(self,staff_id: str, leave_dto: LeaveDTO):
        leave_dict = leave_dto.model_dump(exclude_unset=True)
        leave_dict["staff_id"] = staff_id
        print(leave_dict)
        leave = Leave(**leave_dict)
        print("error")
        result = await self.repository.insert_leave(leave)
        if result:
            return "Leave Added Successfully"
        raise HTTPException(status_code=404, detail="Error Adding Leave !!!")


    async def get_all_leaves(self):
        leave_dicts = await self.repository.find_all_leaves()
        leaves = []

        for leave_dict in leave_dicts:
            staff_dbref = leave_dict["staff_id"]
            staff_name = await self.get_staff_name_from_dbref(staff_dbref)
            leave_dict["staff_name"] = staff_name
            leave = LeaveResponseDTO(**leave_dict)
            leaves.append(leave)  # Append each leave to the list

        return leaves

    

    async def update_leave(self, leave_id: str, leave_update: LeaveDTO):
        leave_dict = leave_update.dict(exclude_unset=True)
        leave = Leave(**leave_dict)

        result = await self.repository.update_leave(leave_id, leave)
        if result:
            return "Leave Updated Successfully"
        raise HTTPException(status_code=404, detail="Error Updating Leave !!!")

    async def approve_leave(self, leave_id: str):
        result = await self.repository.update_leave_status(leave_id, "Approved")
        if result.modified_count == 1:
            return "Leave Approved Successfully"
        raise HTTPException(status_code=404, detail="Leave Not Found or Already Approved !!!")

    async def reject_leave(self, leave_id: str):
        result = await self.repository.update_leave_status(leave_id, "Rejected")
        if result.modified_count == 1:
            return "Leave Rejected Successfully"
        raise HTTPException(status_code=404, detail="Leave Not Found or Already Rejected !!!")
    
    @staticmethod
    async def get_leave_records(date: date) -> List[dict]:
        date_str = date.strftime("%d-%m-%Y")
        leave_records = await LeaveRepository.find_leave_record_for_date(date_str)
        for record in leave_records:
            record['_id'] = str(record['_id'])
        return leave_records
    
    async def get_leave_by_staff_id(self,staff_id:str) -> List[LeaveResponseDTO]:
        leave_records = await LeaveRepository.get_leave_by_staff_id(staff_id)
        if not leave_records:
            raise HTTPException(status_code=404, detail="No leave records found for the given staff ID.")
        leave_response_list = [LeaveResponseDTO(**leave_record) for leave_record in leave_records]
        return leave_response_list

