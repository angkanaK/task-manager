from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token ไม่ถูกต้อง")
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Token ไม่ถูกต้องหรือหมดอายุ")
