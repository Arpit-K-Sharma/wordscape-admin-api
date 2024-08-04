from app.dto.holiday_dto import HolidayDTO, HolidayResponseDTO, YearlyHolidaysDTO, YearlyHolidaysResponseDTO
from app.dto.month_and_year_dto import Month
from app.repository.holiday_repo import HolidayRepository
from fastapi import HTTPException

class HolidayService:
    def __init__(self):
        self.repository = HolidayRepository()

    async def add_holiday(self, holiday: HolidayDTO):
        result = await self.repository.add_holiday(holiday)
        if result.modified_count > 0 or result.upserted_id:
            return "Holiday added successfully"
        raise HTTPException(status_code=400, detail="Failed to add holiday")

    
    async def get_holidays_by_year(self, year: int):
        yearly_holidays = await self.repository.get_holidays_by_year(year)
        if yearly_holidays:
            # Convert to DTO objects
            holidays = [HolidayDTO(**holiday) for holiday in yearly_holidays["holidays"]]
            # Sort holidays by date
            holidays.sort(key=lambda holiday: holiday.date)
            # Convert to response DTO objects
            holidays_response = [HolidayResponseDTO(**holiday.dict()) for holiday in holidays]
            # Create the response DTO
            response_dto = YearlyHolidaysResponseDTO(year=year, holidays=holidays_response)
            return response_dto
        raise HTTPException(status_code=404, detail="Holidays not found for the given year")

    async def get_all_holidays(self):
        all_holidays = await self.repository.get_all_holidays()
        total_holidays = []
        if all_holidays:
            for yearly_holidays in all_holidays:
                holidays = [HolidayDTO(**holiday) for holiday in yearly_holidays["holidays"]]
                holidays.sort(key=lambda holiday: holiday.date)
                holidays_response = [HolidayResponseDTO(**holiday.dict()) for holiday in holidays]
                response_dto = YearlyHolidaysResponseDTO(year=yearly_holidays["year"], holidays=holidays_response)
                total_holidays.append(response_dto)
                




            # return [YearlyHolidaysResponseDTO(**holiday) for holiday in holidays]
            return total_holidays
        raise HTTPException(status_code=404, detail="No holidays found")

    async def update_holiday(self, holiday_id: str, holiday_update: HolidayDTO):
        result = await self.repository.update_holiday(holiday_id, holiday_update)
        if result.modified_count > 0:
            return "Holiday updated successfully"
        raise HTTPException(status_code=404, detail="Holiday not found")
    
    async def delete_holiday(self, holiday_id: str):
        result = await self.repository.delete_holiday(holiday_id)
        if result:
            return "Holiday deleted successfully"
        raise HTTPException(status_code=404, detail="Holiday not found")
    
    async def get_holidays_by_month(self, month: Month):
        result = await self.repository.get_holidays_by_month(month)
        if result: 
            return [HolidayResponseDTO(**holiday) for holiday in result]
        raise HTTPException(status_code=404, detail="Holiday not found for the provided month")


