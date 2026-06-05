from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends

from app import models
from app import auth
from app import schemas

def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    return user

def create_user(db: Session, email, password):
    db_user = models.User(email= email, hashed_password= auth.hash_password(password), role= "user")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user