from pydantic import BaseModel
from typing import Optional
from datetime import date


# ── DEPARTMENT ──────────────────────────────────────────
class DepartmentCreate(BaseModel):
    code: str
    name: str
    head_name: Optional[str] = None
    head_email: Optional[str] = None
    description: Optional[str] = None
    is_pilot: Optional[bool] = False

class DepartmentOut(DepartmentCreate):
    id: int
    class Config:
        from_attributes = True


# ── RESEARCHER ──────────────────────────────────────────
class ResearcherCreate(BaseModel):
    full_name: str
    designation: Optional[str] = None
    department_id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    is_active: Optional[bool] = True

class ResearcherOut(ResearcherCreate):
    id: int
    class Config:
        from_attributes = True


# ── PROJECT ─────────────────────────────────────────────
class ProjectCreate(BaseModel):
    title: str
    department_id: int
    principal_investigator_id: Optional[int] = None
    status: str
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    budget_allocated: Optional[float] = None
    budget_utilized: Optional[float] = None
    funding_source: Optional[str] = None
    objectives: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[str] = None

class ProjectOut(ProjectCreate):
    id: int
    class Config:
        from_attributes = True


# ── MILESTONE ────────────────────────────────────────────
class MilestoneCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: Optional[str] = "Pending"

class MilestoneOut(MilestoneCreate):
    id: int
    class Config:
        from_attributes = True


# ── PROTOTYPE ────────────────────────────────────────────
class PrototypeCreate(BaseModel):
    project_id: int
    name: str
    description: Optional[str] = None
    development_stage: Optional[str] = None
    stage_start_date: Optional[date] = None
    units_produced: Optional[int] = 0
    units_distributed: Optional[int] = 0
    target_crop: Optional[str] = None
    target_region: Optional[str] = None
    notes: Optional[str] = None

class PrototypeOut(PrototypeCreate):
    id: int
    class Config:
        from_attributes = True