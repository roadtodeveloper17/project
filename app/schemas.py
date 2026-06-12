from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length= 8, max_length= 72)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes= True
    
class Token(BaseModel):
    access_token: str
    token_type: str


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes= True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int

class TaskUpdate(BaseModel):
    status: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    project_id: int
    assigned_user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes= True
        