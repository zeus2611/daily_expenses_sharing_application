from sqlalchemy.orm import Session
from app import models
from app.schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = models.User(email=user.email, name=user.name, mobile_number=user.mobile_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
