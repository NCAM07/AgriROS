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



def save_document_record(data: dict):
    db = get_session()
    try:
        from models.models import Document
        doc = Document(**data)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc.id
    finally:
        db.close()


def fetch_project_documents(project_id: int) -> list:
    db = get_session()
    try:
        from models.models import Document
        docs = db.query(Document).filter(
            Document.project_id == project_id
        ).all()
        return [
            {
                "id": d.id,
                "file_name": d.file_name,
                "file_type": d.file_type,
                "document_category": d.document_category,
                "description": d.description,
                "storage_path": d.storage_path,
                "uploaded_by": d.uploaded_by,
                "uploaded_at": d.uploaded_at
            }
            for d in docs
        ]
    finally:
        db.close()


def fetch_all_research():
    db = get_session()
    try:
        from models.models import Research
        records = db.query(Research).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "department_id": r.department_id,
                "supervisor_name": r.supervisor_name,
                "supervisor_designation": r.supervisor_designation,
                "supervisor_email": r.supervisor_email,
                "supervisor_phone": r.supervisor_phone,
                "lead_researcher_name": r.lead_researcher_name,
                "lead_researcher_designation": r.lead_researcher_designation,
                "research_type": r.research_type,
                "status": r.status,
                "start_date": r.start_date,
                "expected_end_date": r.expected_end_date,
                "actual_end_date": r.actual_end_date,
                "objectives": r.objectives,
                "summary": r.summary,
                "keywords": r.keywords,
                "findings": r.findings,
                "funding_source": r.funding_source,
                "funding_amount": r.funding_amount,
                "machine_built": r.machine_built,
                "project_id": r.project_id,
                "journal_name": r.journal_name,
                "publication_date": r.publication_date,
                "doi_or_link": r.doi_or_link,
                "extracted_from_document": r.extracted_from_document,
                "extraction_confirmed": r.extraction_confirmed,
            }
            for r in records
        ]
    finally:
        db.close()


def add_research(data: dict):
    db = get_session()
    try:
        from models.models import Research
        record = Research(**data)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record.id
    finally:
        db.close()


def save_staging(data: dict):
    db = get_session()
    try:
        from models.models import ExtractionStaging
        staging = ExtractionStaging(**data)
        db.add(staging)
        db.commit()
        db.refresh(staging)
        return staging.id
    finally:
        db.close()


def fetch_pending_staging():
    db = get_session()
    try:
        from models.models import ExtractionStaging
        records = db.query(ExtractionStaging).filter(
            ExtractionStaging.status == "Pending Confirmation"
        ).all()
        return [
            {
                "id": r.id,
                "document_id": r.document_id,
                "extracted_title": r.extracted_title,
                "extracted_lead_researcher": r.extracted_lead_researcher,
                "extracted_supervisor": r.extracted_supervisor,
                "extracted_keywords": r.extracted_keywords,
                "extracted_summary": r.extracted_summary,
                "extracted_objectives": r.extracted_objectives,
                "extracted_findings": r.extracted_findings,
                "extracted_funding_source": r.extracted_funding_source,
                "extracted_journal": r.extracted_journal,
                "extracted_publication_date": r.extracted_publication_date,
                "extracted_start_date": r.extracted_start_date,
                "extracted_end_date": r.extracted_end_date,
                "extracted_research_type": r.extracted_research_type,
                "status": r.status,
                "submitted_by": r.submitted_by,
            }
            for r in records
        ]
    finally:
        db.close()


def confirm_staging(staging_id: int, confirmed_by: str, data: dict):
    db = get_session()
    try:
        from models.models import ExtractionStaging, Research
        from sqlalchemy.sql import func
        staging = db.query(ExtractionStaging).filter(
            ExtractionStaging.id == staging_id
        ).first()
        if staging:
            staging.status = "Confirmed"
            staging.confirmed_by = confirmed_by
            staging.confirmed_at = func.now()
            db.commit()

        research = Research(**data)
        db.add(research)
        db.commit()
        db.refresh(research)
        return research.id
    finally:
        db.close()


def reject_staging(staging_id: int):
    db = get_session()
    try:
        from models.models import ExtractionStaging
        staging = db.query(ExtractionStaging).filter(
            ExtractionStaging.id == staging_id
        ).first()
        if staging:
            staging.status = "Rejected"
            db.commit()
    finally:
        db.close()


def fetch_summary():
    db = get_session()
    try:
        total_projects = db.query(Project).count()
        ongoing_projects = db.query(Project).filter(
            Project.status == "Ongoing"
        ).count()
        completed_projects = db.query(Project).filter(
            Project.status == "Completed"
        ).count()
        commercialized = db.query(Project).filter(
            Project.status == "Commercialized"
        ).count()
        pending = db.query(Project).filter(
            Project.status == "Pending Evaluation"
        ).count()
        behind = db.query(Project).filter(
            Project.status == "Behind Schedule"
        ).count()
        abandoned = db.query(Project).filter(
            Project.status == "Abandoned"
        ).count()

        from models.models import Research
        total_research = db.query(Research).count()
        published = db.query(Research).filter(
            Research.status == "Published"
        ).count()
        ongoing_research = db.query(Research).filter(
            Research.status == "Ongoing"
        ).count()

        return {
            "total_projects": total_projects,
            "ongoing_projects": ongoing_projects,
            "completed_projects": completed_projects,
            "commercialized": commercialized,
            "pending": pending,
            "behind": behind,
            "abandoned": abandoned,
            "total_research": total_research,
            "published_research": published,
            "ongoing_research": ongoing_research,
        }
    finally:
        db.close()