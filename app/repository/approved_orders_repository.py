from app.config.db_config import orders_collection
from app.config.db_config import database
from app.dto.approved_orders_dto import ApprovedOrdersDTO

class ApprovedOrdersRepository:
    async def fetch_all_approved_orders():
        approved_orders = []
        cursor = database["order"].find({"status": "APPROVED"})
        async for order in cursor:
            order["_id"] = str(order["_id"]) 
            approved_orders.append(order)
        return [ApprovedOrdersDTO.from_order_collection(order) for order in approved_orders]