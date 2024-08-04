import calendar
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from app.dto.month_and_year_dto import Month
from app.dto.payroll_dto import PayrollDTO
from app.repository.attendance_repo import AttendanceRepository
from app.repository.holiday_repo import HolidayRepository
from app.repository.payroll_repo import PayrollRepository
from app.repository.staff_repo import StaffRepository

class PayrollService:
    def __init__(self):
        self.payroll_repository = PayrollRepository()


    async def generate_payroll(self) -> str:
        active_staffs = await self.get_active_staffs()
        payrollDto = await self.convert_to_payroll_dto(active_staffs)
        return await self.create_calculated_payroll(payrollDto)

    

    async def convert_to_payroll_dto(self,active_staffs):
        payroll_dtos = []
        current_month_year = self.get_current_month_and_year()
        current_month_str = str(current_month_year[0]).zfill(2) 
        current_year_str = str(current_month_year[1]).zfill(4) 
        month_instance = Month(month=current_month_year[0], year=current_month_year[1])

        total_holidays_for_month = await self.get_holidays_for_month(month_instance)
        total_weekends_for_month = self.calculate_weekends(current_month_year[1],current_month_year[0])

        for record in active_staffs:
            staff_id = str(record["_id"])
            staff_name = record["fullName"]
            daily_wage = record["dailyWage"]
            attendance = await self.get_monthly_attendance_by_staffId(staff_id, current_month_year[1], current_month_year[0])
            working_days = attendance["Present"]
            paid_leaves = attendance["Paid Leave"]
            holidays = total_holidays_for_month
            weekends = total_weekends_for_month

            payroll_dto = PayrollDTO(
                staff_id=staff_id,
                staff_name=staff_name,
                month=current_month_str,
                year=current_year_str,
                working_days=working_days,
                paid_leaves=paid_leaves,
                holidays=holidays,
                weekends=weekends,
                daily_wage=daily_wage,
            )

            payroll_dtos.append(payroll_dto)

        return payroll_dtos

    async def get_active_staffs(self):
        return await StaffRepository.find_active_staffs()
    
    async def get_holidays_for_month(self,month: Month) -> int:
        total_holidays = await HolidayRepository.get_holidays_by_month(month)
        return len(total_holidays) if total_holidays else 0
    
    async def get_monthly_attendance_by_staffId(self, staff_id:str, year:int, month:int):
        attendance_records = await AttendanceRepository.get_staff_attendance(staff_id, year, month)

        working_days = 0
        paid_leaves = 0

        for record in attendance_records:
            for staff in record['staffs']:
                if staff['status'] == 'Present':
                    working_days += 1
                elif staff['status'] == 'Paid Leave':
                    paid_leaves += 1

        return {
            "Present": working_days,
            "Paid Leave": paid_leaves
        }
    
    def get_current_month_and_year(self) -> list[int]:
        now = datetime.now()
        return [now.month, now.year] 
    
    async def create_payroll(self, payroll: PayrollDTO) -> str:
        try:
            return await self.payroll_repository.create(payroll)    
        except Exception as e:
            # Log the error
            print(f"Error creating payroll: {str(e)}")
            raise e

    async def get_payroll(self, payroll_id: str) -> Optional[PayrollDTO]:
        try:
            payroll = await self.payroll_repository.read(payroll_id)
            if not payroll:
                print(f"Payroll not found: {payroll_id}")
            return payroll
        except ValueError as e:
            print(f"Invalid payroll ID: {str(e)}")
            raise e
        except Exception as e:
            print(f"Error retrieving payroll: {str(e)}")
            raise e


    async def update_payroll(self, payroll_id:str, payroll: PayrollDTO) -> bool:
        try:
            updated = await self.payroll_repository.update(payroll_id, payroll)
            if not updated:
                print(f"Payroll not found: {payroll_id}")
            return updated
        except ValueError as e:
            print(f"Invalid payroll data: {str(e)}")
            raise e
        except Exception as e:
            print(f"Error updating payroll: {str(e)}")
            raise e


    async def delete_payroll(self, payroll_id: str) -> bool:
        try:
            deleted = await self.payroll_repository.delete(payroll_id)
            if not deleted:
                print(f"Payroll not found: {payroll_id}")
            return deleted
        except ValueError as e:
            print(f"Invalid payroll ID: {str(e)}")
            raise e
        except Exception as e:
            print(f"Error deleting payroll: {str(e)}")
            raise e
        


    async def delete_all_payroll(self) -> bool:
        try:
            # Call the method to delete all payroll records
            deleted_count = await self.payroll_repository.delete_all()
            
            if deleted_count == 0:
                print("No payroll records found to delete.")
                return False
            
            print(f"Successfully deleted {deleted_count} payroll records.")
            return True
        except Exception as e:
            print(f"Error deleting payroll records: {str(e)}")
            raise e


    async def list_all_payrolls(self) -> List[PayrollDTO]:
        try:
            return await self.payroll_repository.list_all()
        except Exception as e:
            print(f"Error listing payrolls: {str(e)}")
            raise e
        
    def calculate_weekends(self, year: int, month: int) -> int:
        try:
            # Validate month and year
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")

            # Get the calendar for the month
            cal = calendar.monthcalendar(year, month)
            
            # Count the number of Saturdays (index 5 of each week)
            saturdays = sum(1 for week in cal if week[calendar.SATURDAY] != 0)
            
            return saturdays
        except ValueError as e:
            print(f"Invalid input: {str(e)}")
            raise e
        except Exception as e:
            print(f"Error calculating weekends: {str(e)}")
            raise e

    async def calculate_payroll(self, payroll: PayrollDTO) -> PayrollDTO:
        # Calculate sub_total
        payroll.sub_total = payroll.daily_wage * (payroll.working_days + payroll.paid_leaves + payroll.weekends + payroll.holidays)

        payroll.tax = payroll.sub_total * 0.01

        # Calculate net_salary
        payroll.net_salary = payroll.sub_total - payroll.tax

        return payroll

    async def create_calculated_payroll(self, payrolls: List[PayrollDTO]) -> str:
        for payroll in payrolls:
            calculated_payroll = await self.calculate_payroll(payroll)
            await self.create_payroll(calculated_payroll)
        return "Payroll Succesfully Uploaded"

    async def update_calculated_payroll(self,payroll_id:str, payroll: PayrollDTO) -> bool:
        calculated_payroll = await self.calculate_payroll(payroll)
        return await self.update_payroll(payroll_id, calculated_payroll)
    
    async def get_payroll_by_month(self, month: str) -> Optional[PayrollDTO]:
        return await self.payroll_repository.get_payroll_by_month(month)
    
    async def get_payroll_by_staff_id(self, staff_id:str) -> List[PayrollDTO]:
        payroll_records = await PayrollRepository.get_payroll_by_staff_id(staff_id)
        if not payroll_records:
            raise HTTPException(status_code=404, detail="No payroll records found for the given staff ID.")
        payroll_response_list = [PayrollDTO(**payroll_record) for payroll_record in payroll_records]
        return payroll_response_list