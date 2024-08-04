from bson import ObjectId
from typing import List, Optional
from app.dto.payroll_dto import PayrollDTO
from pymongo.errors import PyMongoError
from app.config.db_config import payroll_collection

class PayrollRepository:

    async def create(self, payroll: PayrollDTO) -> str:
        try:
            payroll_dict = payroll.dict(by_alias=True)  # Use alias to handle '_id'
            payroll_id = payroll_dict.pop('_id', None)  

            # Create filter criteria
            filter_criteria = {"_id": ObjectId(payroll_id)} if payroll_id else {"staff_id": payroll_dict["staff_id"], "month": payroll_dict["month"]}

            # Update data
            update_data = {"$set": payroll_dict}

            # Perform upsert operation
            result = await payroll_collection.update_one(filter_criteria, update_data, upsert=True)

            if result.upserted_id:
                return str(result.upserted_id)  # Return the ID of the inserted document
            else:
                return f"Payroll with ID {payroll_id} updated successfully."

        except PyMongoError as e:   
            raise Exception(f"Failed to upsert payroll: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing payroll: {str(e)}")

    async def read(self, payroll_id: str) -> Optional[PayrollDTO]:
        try:
            payroll = await payroll_collection.find_one({"_id": ObjectId(payroll_id)})
            if payroll:
                return PayrollDTO(**payroll)
            return None
        except PyMongoError as e:
            raise Exception(f"Failed to read payroll: {str(e)}")
        except ValueError:
            raise ValueError(f"Invalid payroll_id format: {payroll_id}")

    async def update(self,payroll_id:str, payroll: PayrollDTO) -> bool:
        try:
            payroll_dict = payroll.dict()
            payroll_id = ObjectId(payroll_id)
            result = await payroll_collection.update_one(
                {"_id": payroll_id},
                {"$set": payroll_dict}
            )
            if result.modified_count > 0:
                return "Payroll Updated Successfully !!!"
        except PyMongoError as e:
            raise Exception(f"Failed to update payroll: {str(e)}")
        except ValueError:
            raise ValueError(f"Invalid payroll_id format: {payroll.payroll_id}")



    async def delete(self, payroll_id: str) -> bool:
        try:
            # Ensure the ID is a valid ObjectId
            obj_id = ObjectId(payroll_id)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid payroll_id format: {payroll_id}") from e

        try:
            # Perform the delete operation
            result = await payroll_collection.delete_one({"_id": obj_id})
            
            # Check if a document was deleted
            if result.deleted_count > 0:
                return True
            else:
                return False
        except PyMongoError as e:
            raise Exception(f"Failed to delete payroll: {str(e)}")

        
        
    async def delete_all(self) -> str:
        try:
            # Perform the deletion of all documents in the collection
            result = await payroll_collection.delete_many({})
            if result.deleted_count > 0:
                return f"All payroll records deleted successfully! Deleted count: {result.deleted_count}"
            else:
                return "No payroll records found to delete."
        except PyMongoError as e:
            raise Exception(f"Failed to delete payroll records: {str(e)}")

    async def list_all(self) -> List[PayrollDTO]:
        try:
            payrolls = []
            async for payroll in payroll_collection.find():
                payrolls.append(PayrollDTO(**payroll))
            return payrolls
        except PyMongoError as e:
            raise Exception(f"Failed to list payrolls: {str(e)}")
        
    async def get_payroll_by_month(self, month: str) -> Optional[PayrollDTO]:
        try:
            payroll = await payroll_collection.find_one({"month": month})
            if payroll:
                return PayrollDTO(**payroll)
            return None
        except PyMongoError as e:
            raise Exception(f"Failed to retrieve payroll for month {month}: {str(e)}")

    @staticmethod
    async def get_payroll_by_staff_id(staff_id:str):  
        payrolls = await payroll_collection.find({"staff_id": staff_id}).to_list(length=None)
        return payrolls