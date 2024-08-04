from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List

from app.dto.attendance_dto import AttendanceDTO, AttendanceResponseDTO
from app.service.attendance_service import AttendanceService
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification

attendance_route = APIRouter()
logger = get_logger()

@attendance_route.post("/attendance", response_model=str)
async def create_attendance(attendance: AttendanceDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /ATTENDANCE (POST) \n DATA SENT: {attendance.dict()}")
    response = await AttendanceService.create_attendance(attendance)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", message="Attendance Added Successfully", status_code=200)

@attendance_route.get("/attendance/{attendance_date}", response_model=AttendanceResponseDTO)
async def get_attendance(attendance_date: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /ATTENDANCE/{attendance_date} (GET)")
    attendance = await AttendanceService.get_attendance(attendance_date)
    if not attendance:
        logger.error(f"ATTENDANCE NOT FOUND: Date {attendance_date}")
        raise HTTPException(status_code=404, detail="Attendance not found")
    logger.info(f"ATTENDANCE RECORD RETRIEVED: Date {attendance_date}")
    return get_response(status="success", status_code=200, data=attendance)

@attendance_route.get("/attendance/{staff_id}/{year}/{month}", response_model=List[AttendanceDTO])
async def get_staff_attendance(staff_id: str, year: int, month: int, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /ATTENDANCE/{staff_id}/{year}/{month} (GET)")
    attendance_list = await AttendanceService.get_staff_attendance(staff_id, year, month)
    if not attendance_list:
        logger.error(f"NO ATTENDANCE RECORDS FOUND: Staff ID {staff_id}, Year {year}, Month {month}")
        raise HTTPException(status_code=404, detail="No attendance records found for this staff member in the specified month")
    logger.info(f"ATTENDANCE RECORDS RETRIEVED: Staff ID {staff_id}, Year {year}, Month {month}")
    return get_response(status="success", status_code=200, data=attendance_list)
