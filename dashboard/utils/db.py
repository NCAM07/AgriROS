import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from database import SessionLocal
from models.models import (
    Department, Researcher, Project,
    Milestone, Prototype
)


def get_session():
    return SessionLocal()


def fetch_summary():
    db = get_session()
    try:
        total = db.query(Project).count()
        ongoing = db.query(Project).filter(Project.status == "Ongoing").count()
        completed = db.query(Project).filter(Project.status == "Completed").count()
        commercialized = db.query(Project).filter(Project.status == "Commercialized").count()
        pending = db.query(Project).filter(Project.status == "Pending Evaluation").count()
        behind = db.query(Project).filter(Project.status == "Behind Schedule").count()
        abandoned = db.query(Project).filter(Project.status == "Abandoned").count()
        return {
            "total": total,
            "ongoing": ongoing,
            "completed": completed,
            "commercialized": commercialized,
            "pending": pending,
            "behind": behind,
            "abandoned": abandoned
        }
    finally:
        db.close()


def fetch_all_projects():
    db = get_session()
    try:
        projects = db.query(Project).all()
        return [
            {
                "id": p.id,
                "title": p.title,
                "department_id": p.department_id,
                "supervisor_name": p.supervisor_name,
                "supervisor_designation": p.supervisor_designation,
                "supervisor_email": p.supervisor_email,
                "supervisor_phone": p.supervisor_phone,
                "lead_researcher_name": p.lead_researcher_name,
                "lead_researcher_designation": p.lead_researcher_designation,
                "status": p.status,
                "start_date": p.start_date,
                "expected_end_date": p.expected_end_date,
                "actual_end_date": p.actual_end_date,
                "budget_allocated": p.budget_allocated,
                "budget_utilized": p.budget_utilized,
                "funding_source": p.funding_source,
                "keywords": p.keywords,
                "summary": p.summary,
                "machine_built": p.machine_built,
                "prototype_id": p.prototype_id,
            }
            for p in projects
        ]
    finally:
        db.close()


def fetch_all_departments():
    db = get_session()
    try:
        depts = db.query(Department).all()
        return [{"id": d.id, "code": d.code, "name": d.name, "is_pilot": d.is_pilot} for d in depts]
    finally:
        db.close()


def fetch_prototypes():
    db = get_session()
    try:
        prototypes = db.query(Prototype).all()
        return [
            {
                "id": p.id,
                "project_id": p.project_id,
                "name": p.name,
                "development_stage": p.development_stage,
                "units_produced": p.units_produced,
                "units_distributed": p.units_distributed,
                "target_crop": p.target_crop,
                "target_region": p.target_region,
                "notes": p.notes
            }
            for p in prototypes
        ]
    finally:
        db.close()


def add_project(data: dict):
    db = get_session()
    try:
        project = Project(**data)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project.id
    finally:
        db.close()


def add_milestone(data: dict):
    db = get_session()
    try:
        milestone = Milestone(**data)
        db.add(milestone)
        db.commit()
        db.refresh(milestone)
        return milestone.id
    finally:
        db.close()


def add_prototype(data: dict):
    db = get_session()
    try:
        prototype = Prototype(**data)
        db.add(prototype)
        db.commit()
        db.refresh(prototype)
        return prototype.id
    finally:
        db.close()



def fetch_all_researchers():
    db = get_session()
    try:
        researchers = db.query(Researcher).all()
        return [
            {
                "id": r.id,
                "full_name": r.full_name,
                "designation": r.designation,
                "department_id": r.department_id,
                "email": r.email,
                "phone": r.phone,
                "specialization": r.specialization,
                "linkedin": r.linkedin,
                "researchgate": r.researchgate,
                "other_handle": r.other_handle,
                "is_active": r.is_active
            }
            for r in researchers
        ]
    finally:
        db.close()


def add_researcher(data: dict):
    db = get_session()
    try:
        researcher = Researcher(**data)
        db.add(researcher)
        db.commit()
        db.refresh(researcher)
        return researcher.id
    finally:
        db.close()