from app.config.db_config import user_collection

class AdminRepository:

    @staticmethod
    async def get_admin() -> dict:
        admin = await user_collection.find_one({"role":"ROLE_ADMIN"})
        return admin