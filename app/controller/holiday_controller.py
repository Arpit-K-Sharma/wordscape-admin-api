from fastapi import APIRouter, Depends, HTTPException
from app.dto.holiday_dto import HolidayResponseDTO, YearlyHolidaysResponseDTO, HolidayDTO
from app.dto.month_and_year_dto import Month
from app.service.holiday_service import HolidayService
from typing import List
from app.utils.response_util import get_response
from app.config.logger_config import get_logger
from app.utils.auth_utils import admin_verification

holiday_route = APIRouter()
holiday_service = HolidayService()
logger = get_logger()

@holiday_route.post("/holidays")
async def add_holiday(holiday: HolidayDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /HOLIDAYS (POST) \n DATA SENT: {holiday.dict()} \n ADMIN TOKEN: {payload}")
    response = await holiday_service.add_holiday(holiday)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@holiday_route.get("/holidays/{year}", response_model=YearlyHolidaysResponseDTO)
async def get_holidays_by_year(year: int, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /HOLIDAYS/{year} (GET)")
    response = await holiday_service.get_holidays_by_year(year)
    logger.info(f"RESPONSE SENT: Retrieved holidays for year {year}")
    return get_response(status="success", status_code=200, data=response)

@holiday_route.get("/holidays", response_model=List[YearlyHolidaysResponseDTO])
async def get_all_holidays(payload: dict = Depends(admin_verification)):
    logger.info("ENDPOINT CALLED: /HOLIDAYS (GET)")
    response = await holiday_service.get_all_holidays()
    logger.info(f"RESPONSE SENT: Retrieved {len(response)} yearly holidays")
    return get_response(status="success", status_code=200, data=response)

@holiday_route.put("/holidays/{holiday_id}")
async def update_holiday(holiday_id: str, holiday_update: HolidayDTO, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /HOLIDAYS/{holiday_id} (PUT) \n DATA SENT: {holiday_update.dict()}")
    response = await holiday_service.update_holiday(holiday_id, holiday_update)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@holiday_route.delete("/holidays/{holiday_id}")
async def delete_holiday(holiday_id: str, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /HOLIDAYS/{holiday_id} (DELETE)")
    response = await holiday_service.delete_holiday(holiday_id)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, message=response)

@holiday_route.post("/holidays/month")
async def get_holiday_by_month(month: Month, payload: dict = Depends(admin_verification)):
    logger.info(f"ENDPOINT CALLED: /HOLIDAYS/MONTH (POST) \n DATA SENT: {month.dict()}")
    response = await holiday_service.get_holidays_by_month(month)
    logger.info(f"RESPONSE SENT: {response}")
    return get_response(status="success", status_code=200, data=response)
