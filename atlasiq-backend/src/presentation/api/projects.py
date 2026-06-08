from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from src.infrastructure.database.config import get_db
from src.infrastructure.database.repositories import ProjectRepository

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

class ProjectCreate(BaseModel):
    name: str
    budget: float

class ProjectResponse(BaseModel):
    id: str
    name: str
    budget: float
    status: str

@router.get("", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    projects = repo.get_all()
    return [
        ProjectResponse(id=p.id, name=p.name, budget=p.budget, status=p.status)
        for p in projects
    ]

@router.post("", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    new_project = repo.create(name=project.name, budget=project.budget)
    return ProjectResponse(
        id=new_project.id,
        name=new_project.name,
        budget=new_project.budget,
        status=new_project.status
    )

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    p = repo.get_by_id(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(id=p.id, name=p.name, budget=p.budget, status=p.status)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, project: ProjectCreate, db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    p = repo.update(project_id, project.name, project.budget, "planning")
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(id=p.id, name=p.name, budget=p.budget, status=p.status)

@router.delete("/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    success = repo.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
