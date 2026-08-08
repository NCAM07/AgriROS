from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Prototype
from schemas.schemas import PrototypeCreate, PrototypeOut
from typing import List

router = APIRouter(prefix="/prototypes", tags=["Prototypes"])

@router.get("/project/{project_id}", response_model=List[PrototypeOut])
def get_prototypes(project_id: int, db: Session = Depends(get_db)):
    return db.query(Prototype).filter(
        Prototype.project_id == project_id
    ).all()

@router.post("/", response_model=PrototypeOut)
def create_prototype(prototype: PrototypeCreate, db: Session = Depends(get_db)):
    new_prototype = Prototype(**prototype.model_dump())
    db.add(new_prototype)
    db.commit()
    db.refresh(new_prototype)
    return new_prototype