from app.utils.auth_utils import verify_password
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from app.models.adminauth import AdminAuth
from app.repository.admin_repository import AdminRepository

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    to_encode.update({"role": "admin"}) 
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def admin_login(email: str, password: str):
    admin = await AdminRepository.get_admin()
    if admin and email == admin['email'] and verify_password(password, admin["password"]):
        access_token = create_access_token(data={"sub": email})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid credentials")

# async def staff_login(email: str, password: str):
#     if email == "staff@gmail.com" and password == "staffpassword":  
#         access_token = create_access_token(data={"sub": email, "role": "staff"}) 
#         return {"access_token": access_token, "token_type": "bearer"}
#     raise HTTPException(status_code=400, detail="Invalid credentials")


