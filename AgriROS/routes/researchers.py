from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Researcher
from schemas.schemas import ResearcherCreate, ResearcherOut
from typing import List

router = APIRouter(prefix="/researchers", tags=["Researchers"])

@router.get("/", response_model=List[ResearcherOut])
def get_all_researchers(db: Session = Depends(get_db)):
    return db.query(Researcher).all()

@router.get("/{researcher_id}", response_model=ResearcherOut)
def get_researcher(researcher_id: int, db: Session = Depends(get_db)):
    researcher = db.query(Researcher).filter(
        Researcher.id == researcher_id
    ).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return researcher

@router.post("/", response_model=ResearcherOut)
def create_researcher(researcher: ResearcherCreate, db: Session = Depends(get_db)):
    new_researcher = Researcher(**researcher.model_dump())
    db.add(new_researcher)
    db.commit()
    db.refresh(new_researcher)
    return new_researcher