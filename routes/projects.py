from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Project
from schemas.schemas import ProjectCreate, ProjectOut
from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectOut])
def get_all_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/department/{dept_id}", response_model=List[ProjectOut])
def get_projects_by_department(dept_id: int, db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.department_id == dept_id).all()

@router.get("/status/{status}", response_model=List[ProjectOut])
def get_projects_by_status(status: str, db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.status == status).all()

@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    updated: ProjectCreate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in updated.model_dump().items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project