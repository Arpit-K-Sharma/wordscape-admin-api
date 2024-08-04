from fastapi import APIRouter, HTTPException
from app.service.user_service import UserService, CoverTreatmentService, PaperService

user_route = APIRouter()

@user_route.get('/get/user/{id}')
async def get_user(id: str):
    response = await UserService.get_fullName(id)
    return {"message": "User Fetched Successfully", "data": {"fullName": response}}

@user_route.get('/get/coverTreatment/{id}')
async def get_coverTreatment(id: str):
    response = await CoverTreatmentService.get_cover_treatment(id)
    return {"message": "Cover Treatment Fetched Successfully", "data": {"coverTreatmentType": response}}

@user_route.get('/get/paper/{id}')
async def get_paper(id: str):
    response = await PaperService.get_paper(id)
    return {
        "message": "Paper Fetched Successfully",
        "data": {"paperType": response}
    }
