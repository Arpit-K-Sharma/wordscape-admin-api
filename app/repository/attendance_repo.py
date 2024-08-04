from bson import ObjectId
from typing import List, Optional
from app.config.db_config import attendance_collection
from datetime import datetime,date

class AttendanceRepository:

    @staticmethod
    async def create_or_update_attendance(attendance_data: dict):
        attendance_date = attendance_data.get("date")
        result = await attendance_collection.update_one(
            {"date": attendance_date},
            {"$set": attendance_data},
            upsert=True
        )

        return result


    @staticmethod
    async def get_attendance(attendance_date: str) -> Optional[dict]:
        attendance = await attendance_collection.find_one({"date": attendance_date})
        if attendance:
            attendance['_id'] = str(attendance['_id'])
        return attendance
    
    @staticmethod
    async def get_staff_attendance(staff_id: str, year: int, month: int) -> List[dict]:
        
        month_str = f"{month:02d}"

        pipeline = [
            {
                "$match": {
                    "date": {
                        "$regex": f"^\d{{2}}-{month_str}-{year}$"
                    }
                }
            },
            {
                "$project": {
                    "date": 1,
                    "staffs": {
                        "$filter": {
                            "input": "$staffs",
                            "as": "staff",
                            "cond": { "$eq": ["$$staff.staff_id", staff_id] }
                        }
                    }
                }
            },
            {
                "$match": {
                    "staffs": { "$ne": [] }
                }
            }
        ]

        result = await attendance_collection.aggregate(pipeline).to_list(None)
        return result

    

