from app.config.db_config import staff_collection

class AdminRepository:

    @staticmethod
    async def get_admin() -> dict:
        return await staff_collection.find_one({"role":"ROLE_ADMIN"})
