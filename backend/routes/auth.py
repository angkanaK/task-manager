from datetime import datetime, timedelta
from jose import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models
import bcrypt

router = APIRouter()


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email นี้ถูกใช้แล้ว")

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password.decode("utf-8")
    )
    db.add(new_user)
    db.commit()
    return {"message": "สมัครสมาชิกสำเร็จ!"}


router = APIRouter()

SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email นี้ถูกใช้แล้ว")

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password.decode("utf-8")
    )
    db.add(new_user)
    db.commit()
    return {"message": "สมัครสมาชิกสำเร็จ!"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Email หรือรหัสผ่านไม่ถูกต้อง")

    if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(
            status_code=401, detail="Email หรือรหัสผ่านไม่ถูกต้อง")

    token = create_access_token({"user_id": db_user.id})

    return {
        "message": "เข้าสู่ระบบสำเร็จ!",
        "access_token": token,
        "username": db_user.username
    }
