from datetime import datetime, time
from pydantic import BaseModel, validator
from typing import List, Optional

class StaffAttendanceDTO(BaseModel):
    staff_id: str
    staff_name: Optional[str] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    status: str
    remarks: Optional[str] = None

class AttendanceDTO(BaseModel):
    date: datetime
    staffs: List[StaffAttendanceDTO]

class AttendanceResponseDTO(BaseModel):
    date: str
    staffs: List[StaffAttendanceDTO]


