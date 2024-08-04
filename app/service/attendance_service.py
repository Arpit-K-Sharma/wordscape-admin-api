from datetime import datetime, date
from bson import ObjectId
from fastapi import HTTPException
from typing import Dict, List, Optional
from app.dto.attendance_dto import AttendanceDTO, AttendanceResponseDTO, StaffAttendanceDTO
from app.dto.staff_dto import StaffDTO
from app.repository.attendance_repo import AttendanceRepository
from app.service.leave_service import LeaveService
from app.service.staff_service import StaffService
from app.config.db_config import staff_collection

class AttendanceService:

    @staticmethod
    async def get_staff_attendance(staff_id: str, year: int, month: int) -> List[AttendanceDTO]:
        attendance_records = await AttendanceRepository.get_staff_attendance(staff_id, year, month)
        return [
            AttendanceResponseDTO(
                date=record["date"],
                staffs=[StaffAttendanceDTO(**staff) for staff in record['staffs']]
            )
            for record in attendance_records
        ]
    
    @staticmethod
    async def create_attendance(attendance_dto: AttendanceDTO):
        attendance_data = attendance_dto.dict(by_alias=True,exclude_unset=True)

        attendance_date = attendance_data.get("date")
        if isinstance(attendance_date, datetime):    
            attendance_date_str = attendance_date.strftime("%d-%m-%Y")
        elif isinstance(attendance_date, str):
            # Assuming the date string is already in the correct format "dd-MM-yyyy"
            attendance_date_str = attendance_date
        else:
            raise ValueError("Invalid date format")

        attendance_data["date"] = attendance_date_str

        return await AttendanceRepository.create_or_update_attendance(attendance_data)


    @staticmethod
    async def get_attendance(attendance_date: str) -> Optional[AttendanceResponseDTO]:
        # Parse the provided date
        try:
            provided_date = datetime.strptime(attendance_date, "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use dd-mm-yyyy.")
        

        # Check if the date is today
        today = date.today()
        if provided_date == today:
            today_str = today.strftime("%d-%m-%Y")

            # Check if attendance record exists for today
            attendance = await AttendanceRepository.get_attendance(today_str)

            if attendance:
                attendance = await AttendanceService.add_staff_names_to_attendance(attendance)
                return attendance
            
            # If no attendance record, Get active staff
            active_staffs = await StaffService.get_active_staffs()

            # Check for leave records
            leave_records = await LeaveService.get_leave_records(today) 
            if leave_records:
                # Combine leave records with active staff
                combined_records = AttendanceService.combine_leave_and_active_staff(leave_records, active_staffs)
                return combined_records                
            
            else:
                # Create default attendance data
                attendance = {
                    "date": today_str,
                    "staffs": [
                        {
                            "staff_id": staff.id,
                            "staff_name": staff.fullName,
                            "check_in": "08:00",
                            "check_out": "17:00",
                            "status": "Present",
                            "remarks": ""
                        } for staff in active_staffs
                    ]
                }
                return attendance
                    
        # If the date is not today, return the document for the provided date
        attendance = await AttendanceRepository.get_attendance(attendance_date)
        if not attendance:
            raise HTTPException(status_code=404, detail="Attendance not found for the provided date.")
        
        attendance = await AttendanceService.add_staff_names_to_attendance(attendance)

        return attendance
    

    #HELPER METHOD
    @staticmethod
    def combine_leave_and_active_staff(leave_records, active_staff: List[StaffDTO]):
        staff_list = [{"staff_id": staff.id,
                       "staff_name": staff.fullName,
                        "check_in": "08:00",
                        "check_out": "17:00",
                        "status": "Present",
                        "remarks": ""} for staff in active_staff]
        
        # Create a dictionary to quickly lookup leave information by staff_id
        leave_info = {str(leave['staff_id'].id): leave for leave in leave_records}

        for staff in staff_list:
            staff_id_str = staff["staff_id"]
            if staff_id_str in leave_info:
                leave = leave_info[staff_id_str]
                staff["status"] = leave["type"]
                staff["remarks"] = leave["reason"]
                staff["check_in"] = "08:00"
                staff["check_out"] = "17:00"

        return {
            "date": datetime.now().strftime("%d-%m-%Y"),
            "staffs": staff_list
        }

    @staticmethod
    async def get_staff_name_from_ids(staff_ids: List[str]) -> Dict[str,str]:
        # Convert string IDs to ObjectId
        object_ids = [ObjectId(staff_id) for staff_id in staff_ids]

        # Query the staff collection to get names for the provided staff_ids
        staff_records = await staff_collection.find({"_id": {"$in": object_ids}}).to_list(length=len(staff_ids))
        
        # Create a dictionary mapping staff_id to staff_name
        staff_names = {str(staff["_id"]): staff["fullName"] for staff in staff_records}
        
        return staff_names
    
    @staticmethod
    async def add_staff_names_to_attendance(attendance: dict):
        #Getting the staff name from the staff_ids
        staff_list = attendance.get("staffs")
        staff_ids = [staff["staff_id"] for staff in staff_list]

        staff_names = await AttendanceService.get_staff_name_from_ids(staff_ids)

        # Add staff names to staff list
        for staff in staff_list:
            staff_id = staff["staff_id"]
            staff["staff_name"] = staff_names.get(staff_id)

        # Update attendance with the new staff list
        attendance["staffs"] = staff_list

        return attendance
    

    


