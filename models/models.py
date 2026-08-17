from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    Date, Numeric, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    head_name = Column(String(150))
    head_email = Column(String(150))
    description = Column(Text)
    is_pilot = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    researchers = relationship("Researcher", back_populates="department")
    projects = relationship("Project", back_populates="department")


class Researcher(Base):
    __tablename__ = "researchers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    designation = Column(String(150))
    department_id = Column(Integer, ForeignKey("departments.id"))
    email = Column(String(150))
    phone = Column(String(20))
    specialization = Column(String(200))
    linkedin = Column(String(200))
    researchgate = Column(String(200))
    other_handle = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    department = relationship("Department", back_populates="researchers")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    supervisor_name = Column(String(200))
    supervisor_designation = Column(String(150))
    supervisor_email = Column(String(150))
    supervisor_phone = Column(String(20))
    lead_researcher_name = Column(String(200))
    lead_researcher_designation = Column(String(150))
    status = Column(String(50), nullable=False)
    start_date = Column(Date)
    expected_end_date = Column(Date)
    actual_end_date = Column(Date)
    budget_allocated = Column(Numeric(15, 2))
    budget_utilized = Column(Numeric(15, 2))
    funding_source = Column(String(200))
    objectives = Column(Text)
    summary = Column(Text)
    keywords = Column(String(300))
    machine_built = Column(Boolean, default=False)
    prototype_id = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())

    department = relationship("Department", back_populates="projects")
    milestones = relationship("Milestone", back_populates="project")
    prototypes = relationship("Prototype", back_populates="project")


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    due_date = Column(Date)
    completion_date = Column(Date)
    status = Column(String(50), default="Pending")
    created_at = Column(TIMESTAMP, server_default=func.now())

    project = relationship("Project", back_populates="milestones")


class Prototype(Base):
    __tablename__ = "prototypes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text)
    development_stage = Column(String(100))
    stage_start_date = Column(Date)
    units_produced = Column(Integer, default=0)
    units_distributed = Column(Integer, default=0)
    target_crop = Column(String(150))
    target_region = Column(String(150))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())

    project = relationship("Project", back_populates="prototypes")


class SearchLog(Base):
    __tablename__ = "search_log"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text)
    queried_by = Column(String(150))
    results_returned = Column(Integer)
    queried_at = Column(TIMESTAMP, server_default=func.now())