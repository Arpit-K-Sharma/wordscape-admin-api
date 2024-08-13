from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.staffauth import StaffAuth
from app.service.staff_auth_service import staff_login

staff_auth = APIRouter()

@staff_auth.post("/staff/login")
async def login(staff_auth: StaffAuth):
        return await staff_login(staff_auth.email, staff_auth.password) 