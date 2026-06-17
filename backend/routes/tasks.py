from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: str = ""


class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    status: str = None


@router.post("/")
def create_task(task: TaskCreate, user_id: int, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        status="todo",
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/")
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()
    return tasks


@router.put("/{task_id}")
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="ไม่พบ Task นี้")
    if task.title:
        db_task.title = task.title
    if task.description:
        db_task.description = task.description
    if task.status:
        db_task.status = task.status
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="ไม่พบ Task นี้")
    db.delete(db_task)
    db.commit()
    return {"message": "ลบ Task สำเร็จ!"}
