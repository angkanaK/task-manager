# Task Manager

เว็บแอปสำหรับจัดการงานและ Task ส่วนตัว พัฒนาด้วย Python FastAPI และ JavaScript

## Features
- สมัครสมาชิก / เข้าสู่ระบบ
- เพิ่ม / แก้ไข / ลบ Task
- เปลี่ยนสถานะ Task (Todo, In Progress, Done)
- แต่ละ User เห็นเฉพาะ Task ของตัวเอง

## Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript

## Installation

### Backend
```bash
pip install fastapi uvicorn sqlalchemy pymysql bcrypt python-multipart python-jose
cd backend
python -m uvicorn main:app --reload
```

### Frontend
เปิดไฟล์ `frontend/index.html` ด้วย Live Server

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | สมัครสมาชิก |
| POST | /auth/login | เข้าสู่ระบบ |
| GET | /tasks/ | ดู Task ทั้งหมด |
| POST | /tasks/ | สร้าง Task |
| PUT | /tasks/{id} | แก้ไข Task |
| DELETE | /tasks/{id} | ลบ Task |