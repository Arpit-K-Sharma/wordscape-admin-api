from app.config.db_config import orders_collection
from app.dto.approved_orders_dto import ApprovedOrdersDTO
from app.repository.approved_orders_repository import ApprovedOrdersRepository

class ApprovedOrdersService:
    @staticmethod
    async def fetch_all_approved_orders():
        return await ApprovedOrdersRepository.fetch_all_approved_orders()
     