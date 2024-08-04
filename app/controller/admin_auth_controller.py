from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.adminauth import AdminAuth
from app.service.admin_auth_service import admin_login

admin_route = APIRouter()

@admin_route.post("/admin/login")
async def login(admin_auth: AdminAuth):
        return await admin_login(admin_auth.email, admin_auth.password) 