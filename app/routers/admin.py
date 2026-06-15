from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, crud, database, models, dependencies

router = APIRouter(prefix="/admin", tags= ["Admin"])

@router.get("/users", response_model= list[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db),
              current_user: models.User = Depends(dependencies.require_admin)):
    return crud.get_all_users(db)
    
