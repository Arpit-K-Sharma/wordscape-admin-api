from datetime import datetime
from typing import Dict, List
from bson import ObjectId
from app.config.db_config import holiday_collection
from app.dto.holiday_dto import HolidayDTO, YearlyHolidaysDTO
from app.dto.month_and_year_dto import Month

class HolidayRepository:

    async def add_holiday(self, holiday: HolidayDTO):
        year = holiday.date.year
        holiday_dict = holiday.dict(exclude_unset=True)
        holiday_dict["holiday_id"] = ObjectId()
        result = await holiday_collection.update_one(
            {"year": year},
            {"$push": {"holidays": holiday_dict}},
            upsert=True 
        )
        return result

    async def get_holidays_by_year(self, year: int):
        return await holiday_collection.find_one({"year": year})

    async def get_all_holidays(self):
        cursor = holiday_collection.find({})
        return await cursor.to_list(length=None)

    async def update_holiday(self, holiday_id: str, holiday_update: HolidayDTO):
        holiday_dict = holiday_update.dict(exclude_unset=True)
        holiday_dict["holiday_id"] = ObjectId(holiday_id)
        year = holiday_update.date.year
        return await holiday_collection.update_one(
            {"year": year, "holidays.holiday_id": ObjectId(holiday_id)},
            {"$set": {"holidays.$": holiday_dict}}
        )
    
    async def delete_holiday(self,holiday_id: str):
        result = await holiday_collection.update_one(
            {"holidays.holiday_id": ObjectId(holiday_id)},
            {"$pull": {"holidays": {"holiday_id": ObjectId(holiday_id)}}}
        )
        return result

    @staticmethod
    async def get_holidays_by_month(month: Month) -> List[Dict]:
        # Construct the date range for the query
        start_date = datetime(month.year, month.month, 1)
        if month.month == 12:
            end_date = datetime(month.year + 1, 1, 1)
        else:
            end_date = datetime(month.year, month.month + 1, 1)

        # Create the MongoDB query
        query = {
            "year": month.year,
            "holidays": {
                "$elemMatch": {
                    "date": {
                        "$gte": start_date,
                        "$lt": end_date
                    }
                }
            }
        }

        # Execute the query
        result = await holiday_collection.find_one(query)

        if result:
            # Filter the holidays array to only include holidays in the specified month
            holidays = [
                {
                    "name": holiday['name'],
                    "date": holiday['date'],
                    "description": holiday['description'],
                    "holiday_id": str(holiday['holiday_id'])
                }
                for holiday in result['holidays']
                if start_date <= holiday['date'] < end_date
            ]
            return holidays
        else:
            return []