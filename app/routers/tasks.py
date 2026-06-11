from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import database, models, crud, dependencies, schemas


router = APIRouter(prefix= "/tasks", tags= ["Tasks"])

@router.post("/")
def create_task(task: schemas.TaskCreate, 
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(dependencies.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()

    if not project:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Forbidden")
    
    return crud.create_task(db, task.title, task.description, task.project_id)

@router.