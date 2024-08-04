from app.config.db_config import user_collection
from app.dto.user_dto import UserDTO
from app.repository.user_repository import UserRepository, CoverTreatmentRepository, PaperRepository
from bson import ObjectId

class UserService:
    @staticmethod
    async def get_fullName(user_id: str):
        return await UserRepository.get_fullName(user_id)
    
class CoverTreatmentService:
    @staticmethod
    async def get_cover_treatment(cover_treatment_id: str):
        return await CoverTreatmentRepository.get_cover_treatment(cover_treatment_id)
    
class PaperService:
    @staticmethod
    async def get_paper(paper_id: str):
        return await PaperRepository.get_paper(paper_id)