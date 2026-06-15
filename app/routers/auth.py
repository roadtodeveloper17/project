from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app import auth
from app.database import get_db

router = APIRouter(prefix= "/auth", tags= ["Auth"])

@router.post("/register", response_model= schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Email already registered")
    
    return crud.create_user(db, user.email, user.password)

@router.post("/login", response_model= schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid password")
    
    token = auth.create_access_token(data= {"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}
