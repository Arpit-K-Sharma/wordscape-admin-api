from app.config.db_config import user_collection, cover_collection, paper_collection
from app.dto.user_dto import UserDTO, CoverTreatmentDTO, PaperDTO
from bson import ObjectId

class UserRepository:
    @staticmethod
    async def get_fullName(user_id: str):
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user.get("fullName")
        return None
    
class CoverTreatmentRepository:
    @staticmethod
    async def get_cover_treatment(cover_treatment_id: str):
        cover_treatment = await cover_collection.find_one({"_id": ObjectId(cover_treatment_id)})
        if cover_treatment:
            return cover_treatment.get("coverTreatmentType")
        return None
    
class PaperRepository:
    @staticmethod
    async def get_paper(paper_id: str):
        paper = await paper_collection.find_one({"_id": ObjectId(paper_id)})
        if paper:
            return paper.get("paperType")
        return None