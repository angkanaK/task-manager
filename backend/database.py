from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://task_manager_db_vgec_user:USbys2FkA4gYoXy3e9pt0gLvVVxiKcmi@dpg-d8p5ai1194ac738uufgg-a/task_manager_db_vgec"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
