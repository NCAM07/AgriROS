from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Milestone
from schemas.schemas import MilestoneCreate, MilestoneOut
from typing import List

router = APIRouter(prefix="/milestones", tags=["Milestones"])

@router.get("/project/{project_id}", response_model=List[MilestoneOut])
def get_milestones(project_id: int, db: Session = Depends(get_db)):
    return db.query(Milestone).filter(
        Milestone.project_id == project_id
    ).all()

@router.post("/", response_model=MilestoneOut)
def create_milestone(milestone: MilestoneCreate, db: Session = Depends(get_db)):
    new_milestone = Milestone(**milestone.model_dump())
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)
    return new_milestone