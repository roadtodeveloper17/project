from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models, dependencies, database

router = APIRouter(prefix= "/projects", tags= ["Projects"])

@router.post("/", response_model= schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate,
                   current_user: models.User = Depends(dependencies.get_current_user),
                   db: Session = Depends(database.get_db)):
    if current_user.id != project.owner_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Forbidden")
    
    return crud.create_project(db, project.name, project.description, project.owner_id)

@router.get("/", response_model = list[schemas.ProjectResponse])
def get_my_projects(db: Session = Depends(database.get_db),
                    current_user: models.User = Depends(dependencies.get_current_user)):
    return crud.get_project_by_owner(db, current_user.id)

@router.get("/{project_id}", response_model = schemas.ProjectResponse)
def get_project(project_id: int,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(dependencies.get_current_user)):
    project = crud.get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Forbidden")
    
    return project
