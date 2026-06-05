from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)

    email= Column(String, unique = True, nullable= False, index= True)
    hashed_password = Column(String, nullable= False)
    role = Column(String, default= "user", nullable= False)
    created_at = Column(DateTime(timezone= True), server_default=func.now())

    projects = relationship("Project", back_populates="owner")
    assigned_tasks = relationship("Task", back_populates = "assigned_user")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key = True, index= True)

    name = Column(String, nullable= False)
    description = Column(String, nullable= True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates = "projects")
    tasks = relationship("Task", back_populates= "project")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)

    title = Column(String, nullable= False)
    description = Column(String, nullable= True)
    status = Column(String, default= "todo", nullable= False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable= False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    
    created_at = Column(DateTime(timezone= True), server_default=func.now())

    assigned_user = relationship("User", back_populates = "assigned_tasks")
    project = relationship("Project", back_populates= "tasks")
    

