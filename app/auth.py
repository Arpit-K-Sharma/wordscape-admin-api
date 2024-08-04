import time
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from typing import Optional

SECRET_KEY = "614d0ba902cc93b9d4dc24fff3e2cf6a4ac3c1a2347a54ec32407b2895d840e1"  

security = HTTPBearer()

def create_access_token(data: dict, expires_in: Optional[int] = 3600):
    to_encode = data.copy()
    expire = time.time() + expires_in
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
