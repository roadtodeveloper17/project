from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import database, models, crud, dependencies, schemas


router = APIRouter(prefix= "/tasks", tags= ["Tasks"])

@router.post("/", response_model = schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, 
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(dependencies.get_current_user)):
    project = crud.get_project_by_id(db, task.project_id)

    if not project:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Forbidden")
    
    return crud.create_task(db, task.title, task.description, task.project_id)

@router.get("/project/{project_id}", response_model = list[schemas.TaskResponse])
def get_all_tasks(project_id: int,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(dependencies.get_current_user)):
    project = crud.get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= "Forbidden")
    
    return crud.get_tasks_by_project(db, project_id)

@router.patch("/{task_id}", response_model= schemas.TaskResponse)
def update_task(task_id: int,
                task_update: schemas.TaskUpdate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(dependencies.get_current_user)):
    task = crud.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Task not found")
    
    project = crud.get_project_by_id(db, task.project_id)

    if project.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Forbidden")
    
    return crud.update_task_status(db, task.id, task_update.status)

@router.delete("/{task_id}")
def delete_task(task_id: int,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(dependencies.get_current_user)):
    task = crud.get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Task not found")
    
    project = crud.get_project_by_id(db, task.project_id)

    if project.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Forbidden")
    
    crud.delete_task(db, task_id)
    return {"message": "Task deleted"}