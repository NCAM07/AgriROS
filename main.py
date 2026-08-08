from fastapi import FastAPI
from database import engine
from models.models import Base
from routes import (
    departments,
    researchers,
    projects,
    milestones,
    prototypes
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NCAM Research Intelligence Platform",
    description="Centralized research monitoring for NCAM — Pilot: FPM & ESS",
    version="1.0.0"
)

app.include_router(departments.router)
app.include_router(researchers.router)
app.include_router(projects.router)
app.include_router(milestones.router)
app.include_router(prototypes.router)

@app.get("/")
def root():
    return {
        "platform": "NCAM Research Intelligence Platform",
        "status": "running",
        "pilot_departments": ["FPM", "ESS"],
        "docs": "/docs"
    }

@app.get("/summary")
def summary(db=None):
    from database import SessionLocal
    from models.models import Project
    db = SessionLocal()
    total = db.query(Project).count()
    ongoing = db.query(Project).filter(Project.status == "Ongoing").count()
    completed = db.query(Project).filter(Project.status == "Completed").count()
    commercialized = db.query(Project).filter(
        Project.status == "Commercialized"
    ).count()
    pending = db.query(Project).filter(
        Project.status == "Pending Evaluation"
    ).count()
    behind = db.query(Project).filter(
        Project.status == "Behind Schedule"
    ).count()
    db.close()
    return {
        "total_projects": total,
        "ongoing": ongoing,
        "completed": completed,
        "commercialized": commercialized,
        "pending_evaluation": pending,
        "behind_schedule": behind
    }