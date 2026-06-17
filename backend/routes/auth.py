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

    return {"message": "เข้าสู่ระบบสำเร็จ!", "user_id": db_user.id, "username": db_user.username}
