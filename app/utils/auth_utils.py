from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

load_dotenv()

# Set up CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

def is_admin(payload: dict) -> bool:
    roles = payload.get("role", [])
    return "ROLE_ADMIN" in roles

def is_staff(payload: dict) -> bool:
    roles = payload.get("role", [])
    return "ROLE_STAFF" in roles

async def admin_verification(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not is_admin(payload):
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return payload

async def staff_verification(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not is_staff(payload):
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return payload

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)