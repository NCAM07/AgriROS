import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import sys
import os
from PIL import Image

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from dashboard.utils.db import (
    fetch_summary, fetch_all_projects, fetch_all_departments,
    fetch_all_researchers, fetch_prototypes,
    fetch_all_research, fetch_project_documents,
    add_project, add_researcher, add_milestone,
    add_prototype, add_research,
    save_document_record, save_staging,
    fetch_pending_staging, confirm_staging, reject_staging
)
from dashboard.utils.storage import (
    upload_document, get_document_url
)
from ai_search.search import ai_search, keyword_search
from ai_search.extractor import extract_research_details


# ── PAGE CONFIG ──────────────────────────────────────────────────────
ncam_logo = Image.open("ncam-logo.png")
st.set_page_config(
    page_title="NCAM Research Intelligence Platform",
    page_icon=ncam_logo,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PLACEHOLDER DATA ──────────────────────────────────────────────────────
PLACEHOLDER_PROJECTS = [
    {
        "id": 1,
        "title": "Development of Low-Cost Maize Sheller for Smallholder Farmers",
        "department_id": 1,
        "status": "Completed",
        "supervisor_name": "Dr. Abubakar Musa",
        "supervisor_designation": "Principal Research Officer",
        "supervisor_email": "a.musa@ncam.gov.ng",
        "supervisor_phone": "08012345678",
        "lead_researcher_name": "Engr. Yusuf Abdullahi",
        "lead_researcher_designation": "Senior Research Engineer",
        "start_date": date(2020, 1, 10),
        "expected_end_date": date(2021, 6, 30),
        "actual_end_date": date(2021, 8, 15),
        "budget_allocated": 2500000,
        "budget_utilized": 2300000,
        "funding_source": "FMARD",
        "keywords": "maize, sheller",
        "machine_built": True,
        "prototype_id": 1
    },
    {
        "id": 2,
        "title": "Adaptive Research on Solar-Powered Irrigation Pump Systems",
        "department_id": 1,
        "status": "Ongoing",
        "supervisor_name": "Dr. Suleiman Bello",
        "supervisor_designation": "Chief Research Officer",
        "supervisor_email": "s.bello@ncam.gov.ng",
        "supervisor_phone": "08023456789",
        "lead_researcher_name": "Engr. Fatima Usman",
        "lead_researcher_designation": "Research Engineer",
        "start_date": date(2023, 3, 1),
        "expected_end_date": date(2025, 3, 1),
        "actual_end_date": None,
        "budget_allocated": 5000000,
        "budget_utilized": 2800000,
        "funding_source": "World Bank",
        "keywords": "solar, irrigation",
        "machine_built": False,
        "prototype_id": None
    },
    {
        "id": 3,
        "title": "Evaluation of Tractor-Drawn Cassava Ridger Performance in Nigerian Soils",
        "department_id": 1,
        "status": "Ongoing",
        "supervisor_name": "Dr. Abubakar Musa",
        "supervisor_designation": "Principal Research Officer",
        "supervisor_email": "a.musa@ncam.gov.ng",
        "supervisor_phone": "08012345678",
        "lead_researcher_name": "Engr. Chukwuemeka Obi",
        "lead_researcher_designation": "Research Officer",
        "start_date": date(2022, 6, 15),
        "expected_end_date": date(2024, 6, 15),
        "actual_end_date": None,
        "budget_allocated": 3200000,
        "budget_utilized": 3200000,
        "funding_source": "NCAM Internal",
        "keywords": "cassava, tractor, ridger",
        "machine_built": True,
        "prototype_id": 2
    },
    {
        "id": 4,
        "title": "Fabrication and Testing of Multi-Crop Thresher for Northern Nigeria",
        "department_id": 2,
        "status": "Pending Evaluation",
        "supervisor_name": "Engr. Chioma Okafor",
        "supervisor_designation": "Senior Engineer",
        "supervisor_email": "c.okafor@ncam.gov.ng",
        "supervisor_phone": "08034567890",
        "lead_researcher_name": "Engr. Ibrahim Lawal",
        "lead_researcher_designation": "Research Engineer",
        "start_date": date(2021, 9, 1),
        "expected_end_date": date(2023, 3, 1),
        "actual_end_date": None,
        "budget_allocated": 1800000,
        "budget_utilized": 1750000,
        "funding_source": "FMARD",
        "keywords": "thresher, multi-crop",
        "machine_built": True,
        "prototype_id": 3
    },
    {
        "id": 5,
        "title": "Design of Ergonomic Hand Tools for Female Farmers in Root Crop Production",
        "department_id": 1,
        "status": "Completed",
        "supervisor_name": "Dr. Suleiman Bello",
        "supervisor_designation": "Chief Research Officer",
        "supervisor_email": "s.bello@ncam.gov.ng",
        "supervisor_phone": "08023456789",
        "lead_researcher_name": "Dr. Amina Garba",
        "lead_researcher_designation": "Research Officer",
        "start_date": date(2019, 4, 1),
        "expected_end_date": date(2020, 4, 1),
        "actual_end_date": date(2020, 5, 20),
        "budget_allocated": 900000,
        "budget_utilized": 870000,
        "funding_source": "USAID",
        "keywords": "ergonomic, hand tools, women",
        "machine_built": True,
        "prototype_id": None
    },
    {
        "id": 6,
        "title": "Prototype Development of Motorized Yam Pounding Machine",
        "department_id": 2,
        "status": "Behind Schedule",
        "supervisor_name": "Engr. Chioma Okafor",
        "supervisor_designation": "Senior Engineer",
        "supervisor_email": "c.okafor@ncam.gov.ng",
        "supervisor_phone": "08034567890",
        "lead_researcher_name": "Engr. Taiwo Adeyemi",
        "lead_researcher_designation": "Junior Research Engineer",
        "start_date": date(2022, 1, 1),
        "expected_end_date": date(2023, 6, 30),
        "actual_end_date": None,
        "budget_allocated": 4200000,
        "budget_utilized": 1900000,
        "funding_source": "NCAM Internal",
        "keywords": "yam, motorized, pounding",
        "machine_built": True,
        "prototype_id": 4
    },
    {
        "id": 7,
        "title": "Commercialization of NCAM Jab Planter — Phase II Rollout",
        "department_id": 1,
        "status": "Commercialized",
        "supervisor_name": "Dr. Abubakar Musa",
        "supervisor_designation": "Principal Research Officer",
        "supervisor_email": "a.musa@ncam.gov.ng",
        "supervisor_phone": "08012345678",
        "lead_researcher_name": "Engr. Yusuf Abdullahi",
        "lead_researcher_designation": "Senior Research Engineer",
        "start_date": date(2018, 2, 1),
        "expected_end_date": date(2019, 12, 31),
        "actual_end_date": date(2020, 1, 15),
        "budget_allocated": 6000000,
        "budget_utilized": 5800000,
        "funding_source": "CBN AgriFinance",
        "keywords": "jab planter, commercialization",
        "machine_built": True,
        "prototype_id": None
    },
    {
        "id": 8,
        "title": "Soil Compaction Analysis Under Different Tractor Operations",
        "department_id": 1,
        "status": "Abandoned",
        "supervisor_name": "Dr. Suleiman Bello",
        "supervisor_designation": "Chief Research Officer",
        "supervisor_email": "s.bello@ncam.gov.ng",
        "supervisor_phone": "08023456789",
        "lead_researcher_name": "Engr. Chukwuemeka Obi",
        "lead_researcher_designation": "Research Officer",
        "start_date": date(2020, 7, 1),
        "expected_end_date": date(2021, 12, 31),
        "actual_end_date": None,
        "budget_allocated": 1200000,
        "budget_utilized": 400000,
        "funding_source": "NCAM Internal",
        "keywords": "soil, tractor, compaction",
        "machine_built": False,
        "prototype_id": None
    },
]

PLACEHOLDER_PROTOTYPES = [
    {"id": 1, "project_id": 1, "name": "NCAM Maize Sheller MK-II",
     "development_stage": "Commercialization", "units_produced": 45,
     "units_distributed": 30, "target_crop": "Maize", "target_region": "North Central"},
    {"id": 2, "project_id": 2, "name": "Solar Irrigation Pump Unit A",
     "development_stage": "Testing", "units_produced": 3,
     "units_distributed": 0, "target_crop": "General", "target_region": "Northwest"},
    {"id": 3, "project_id": 4, "name": "Multi-Crop Thresher MT-01",
     "development_stage": "Certification", "units_produced": 5,
     "units_distributed": 0, "target_crop": "Maize, Sorghum", "target_region": "North"},
    {"id": 4, "project_id": 6, "name": "Motorized Yam Pounder YP-01",
     "development_stage": "Fabrication", "units_produced": 1,
     "units_distributed": 0, "target_crop": "Yam", "target_region": "Southwest"},
]

PLACEHOLDER_RESEARCHERS = [
    {"id": 1, "full_name": "Dr. Abubakar Musa", "designation": "Principal Research Officer",
     "department_id": 1, "specialization": "Farm Mechanization"},
    {"id": 2, "full_name": "Engr. Chioma Okafor", "designation": "Senior Engineer",
     "department_id": 2, "specialization": "Prototype Fabrication"},
    {"id": 3, "full_name": "Dr. Suleiman Bello", "designation": "Research Officer",
     "department_id": 1, "specialization": "Soil-Machine Dynamics"},
]

DEPT_MAP = {1: "FPM", 2: "ESS", 3: "PSE", 4: "LWE", 5: "AIDE"}
DEPT_FULL = {
    1: "Farm Power & Machinery",
    2: "Engineering & Scientific Services",
    3: "Processing & Storage Engineering",
    4: "Land & Water Engineering",
    5: "Agro-Industry Development & Extension"
}

STATUS_COLORS = {
    "Ongoing": "#2196F3",
    "Completed": "#4CAF50",
    "Commercialized": "#FF9800",
    "Pending Evaluation": "#9C27B0",
    "Behind Schedule": "#F44336",
    "Abandoned": "#9E9E9E"
}


# ── PAGE CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NCAM Research Intelligence Platform",
    page_icon=ncam_logo,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STYLING ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #F9FFF9; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1B5E20;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #A5D6A7 !important;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #C8E6C9;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    [data-testid="metric-container"] label {
        color: #388E3C !important;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1B5E20 !important;
        font-size: 2rem;
        font-weight: 800;
    }

    /* Section headers */
    .section-header {
        color: #1B5E20;
        font-size: 1.1rem;
        font-weight: 700;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.4rem;
        margin-bottom: 1.2rem;
        margin-top: 1.5rem;
    }

    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Page title */
    .page-title {
        color: #1B5E20;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .page-sub {
        color: #388E3C;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    /* Form styling */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border: 1.5px solid #C8E6C9 !important;
        border-radius: 6px !important;
    }
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #4CAF50 !important;
    }

    /* Buttons */
    .stButton button {
        background-color: #2E7D32 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    .stButton button:hover {
        background-color: #1B5E20 !important;
    }

    /* Dataframe */
    .dataframe { font-size: 0.85rem; }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        color: #2E7D32;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ─────────────────────────────────────────────────────────────
def load_data():
    """Load every dataset independently so one failing table
    (or an empty database) never blanks the whole dashboard."""
    errors = []

    def _safe(fn, default):
        try:
            return fn() or default
        except Exception as e:
            errors.append(f"{fn.__name__}: {e}")
            return default

    projects = _safe(fetch_all_projects, [])
    research = _safe(fetch_all_research, [])
    prototypes = _safe(fetch_prototypes, [])
    researchers = _safe(fetch_all_researchers, [])

    try:
        summary = fetch_summary()
    except Exception as e:
        errors.append(f"fetch_summary: {e}")
        summary = {}

    if errors:
        st.warning("Some records could not be loaded — " + "; ".join(errors))

    using_placeholder = (len(projects) == 0 and len(research) == 0)
    return (
        projects, research, prototypes,
        researchers, summary, using_placeholder
    )


projects, research, prototypes, researchers, summary, using_placeholder = (
    load_data()
)
projects_df = pd.DataFrame(projects) if projects else pd.DataFrame()
research_df = pd.DataFrame(research) if research else pd.DataFrame()
prototypes_df = pd.DataFrame(prototypes) if prototypes else pd.DataFrame()
researchers_df = pd.DataFrame(researchers) if researchers else pd.DataFrame()


# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("ncam-logo.png", width=120)
    st.markdown("**Research Intelligence Platform**")
    st.markdown("---")

    role = st.selectbox(
        "ACCESS LEVEL",
        ["Management View", "Staff View"],
    )

    st.markdown("---")
    st.markdown(
        "<p style='color:#A5D6A7;font-size:0.72rem;"
        "letter-spacing:0.1em;text-transform:uppercase;'>NAVIGATE</p>",
        unsafe_allow_html=True
    )

    all_pages = [
        "Overview",
        "Projects",
        "Research",
        "Prototype Tracker",
        "Researchers",
        "AI Search",
        "Pending Approvals",
        "Update Records",
        "Data Entry"
    ]

    if "page" not in st.session_state:
        st.session_state["page"] = "Overview"

    for p in all_pages:
        if p == "Data Entry" and role == "Management View":
            continue
        is_active = st.session_state["page"] == p
        btn_style = (
            "background:#2E7D32;color:white;border-radius:6px;"
            "padding:0.4rem 0.8rem;margin-bottom:4px;"
            "width:100%;text-align:left;font-weight:600;"
        ) if is_active else (
            "background:transparent;color:white;border-radius:6px;"
            "padding:0.4rem 0.8rem;margin-bottom:4px;"
            "width:100%;text-align:left;"
        )
        if st.button(p, key=f"nav_{p}", use_container_width=True):
            st.session_state["page"] = p
            st.rerun()

    st.markdown("---")
    st.markdown("**Pilot Departments**")
    st.markdown("🟢 Farm Power & Machinery")
    st.markdown("🟢 Engineering & Scientific Services")
    st.markdown("---")
    if using_placeholder:
        st.warning("⚠️ Showing sample data.")
    st.markdown(
        "<small style='color:#A5D6A7'>NCAM · Ilorin · 2026</small>",
        unsafe_allow_html=True
    )

page = st.session_state["page"]


# ══════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown('<div class="page-title">Research Intelligence Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">National Centre for Agricultural Mechanization — Executive Dashboard</div>', unsafe_allow_html=True)

    # ── KPI METRICS ──
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    c1.metric("Total Projects", summary.get("total_projects", 0))
    c2.metric("Ongoing", summary.get("ongoing_projects", 0))
    c3.metric("Completed", summary.get("completed_projects", 0))
    c4.metric("Commercialized", summary.get("commercialized", 0))
    c5.metric("Pending Evaluation", summary.get("pending", 0))
    c6.metric("Behind Schedule", summary.get("behind", 0))
    c7.metric("Abandoned", summary.get("abandoned", 0))

    st.markdown("---")

    if projects_df.empty:
        st.info(
            "No project data yet — add projects via Data Entry "
            "to populate the charts below."
        )
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Project Status Distribution</div>', unsafe_allow_html=True)
        status_counts = projects_df["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_pie = px.pie(
            status_counts,
            names="Status",
            values="Count",
            color="Status",
            color_discrete_map=STATUS_COLORS,
            hole=0.45
        )
        fig_pie.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Projects by Department</div>', unsafe_allow_html=True)
        dept_counts = projects_df["department_id"].map(DEPT_MAP).value_counts().reset_index()
        dept_counts.columns = ["Department", "Projects"]
        fig_bar = px.bar(
            dept_counts,
            x="Department",
            y="Projects",
            color_discrete_sequence=["#2E7D32"],
            text="Projects"
        )
        fig_bar.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False,
            margin=dict(t=10, b=10),
            yaxis=dict(showgrid=True, gridcolor="#E8F5E9")
        )
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── BUDGET UTILIZATION ──
    st.markdown('<div class="section-header">Budget Allocation vs Utilization (₦)</div>', unsafe_allow_html=True)
    budget_df = projects_df[
        projects_df["budget_allocated"].notna()
    ][["title", "budget_allocated", "budget_utilized", "status"]].copy()
    budget_df["title_short"] = budget_df["title"].str[:45] + "..."
    budget_df["utilization_pct"] = (
        budget_df["budget_utilized"] / budget_df["budget_allocated"] * 100
    ).round(1)

    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(
        name="Allocated",
        x=budget_df["title_short"],
        y=budget_df["budget_allocated"],
        marker_color="#C8E6C9"
    ))
    fig_budget.add_trace(go.Bar(
        name="Utilized",
        x=budget_df["title_short"],
        y=budget_df["budget_utilized"],
        marker_color="#2E7D32"
    ))
    fig_budget.update_layout(
        barmode="group",
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(showgrid=True, gridcolor="#E8F5E9"),
        xaxis=dict(tickangle=-30),
        legend=dict(orientation="h"),
        margin=dict(t=10, b=120)
    )
    st.plotly_chart(fig_budget, use_container_width=True)

    # ── RECENT PROJECTS ──
    st.markdown('<div class="section-header">Recent Projects</div>', unsafe_allow_html=True)
    recent = projects_df[["title", "status", "department_id", "start_date", "budget_allocated"]].copy()
    recent["Department"] = recent["department_id"].map(DEPT_MAP)
    recent = recent.drop(columns=["department_id"])
    recent.columns = ["Title", "Status", "Start Date", "Budget (₦)", "Department"]
    recent = recent[["Title", "Department", "Status", "Start Date", "Budget (₦)"]]
    st.dataframe(recent, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 2 — PROJECTS
# ══════════════════════════════════════════════════════════════════════════
elif page == "Projects":
    st.markdown('<div class="page-title">Research Projects</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Full project register — filter by department or status</div>', unsafe_allow_html=True)

    if projects_df.empty:
        st.info("No projects in the database yet. Add one via Data Entry.")
        st.stop()

    col1, col2, col3 = st.columns(3)
    with col1:
        dept_filter = st.selectbox(
            "Filter by Department",
            ["All"] + list(DEPT_MAP.values())
        )
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Ongoing", "Completed", "Commercialized",
             "Pending Evaluation", "Behind Schedule", "Abandoned"]
        )
    with col3:
        search = st.text_input("Search by keyword", placeholder="e.g. cassava, solar...")

    filtered = projects_df.copy()
    if dept_filter != "All":
        filtered = filtered[filtered["department_id"].map(DEPT_MAP) == dept_filter]
    if status_filter != "All":
        filtered = filtered[filtered["status"] == status_filter]
    if search:
        filtered = filtered[
            filtered["title"].str.contains(search, case=False, na=False) |
            filtered["keywords"].astype(str).str.contains(search, case=False, na=False)
        ]

    st.markdown(f"**{len(filtered)} project(s) found**")
    st.markdown("---")

    for _, row in filtered.iterrows():
        machine_label = "🔧 Machine Built" if row.get("machine_built") else "📄 No Machine Yet"
        machine_color = "#2E7D32" if row.get("machine_built") else "#9E9E9E"

        with st.expander(f"📋 {row['title']}"):

            # ── Status + Machine flag ──
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Department:** {DEPT_FULL.get(row['department_id'], 'N/A')}")
            c2.markdown(f"**Status:** {row['status']}")
            c3.markdown(
                f"<span style='background:{machine_color};color:white;"
                f"padding:0.2rem 0.7rem;border-radius:12px;"
                f"font-size:0.78rem;font-weight:600;'>{machine_label}</span>",
                unsafe_allow_html=True
            )

            st.markdown("---")

            # ── Supervisor details ──
            st.markdown("**Principal Supervisor**")
            cs1, cs2, cs3, cs4 = st.columns(4)
            cs1.markdown(f"**Name:** {row.get('supervisor_name', 'N/A')}")
            cs2.markdown(f"**Designation:** {row.get('supervisor_designation', 'N/A')}")
            cs3.markdown(f"**Email:** {row.get('supervisor_email', 'N/A')}")
            cs4.markdown(f"**Phone:** {row.get('supervisor_phone', 'N/A')}")

            st.markdown("---")

            # ── Lead researcher ──
            st.markdown("**Lead Researcher**")
            cl1, cl2 = st.columns(2)
            cl1.markdown(f"**Name:** {row.get('lead_researcher_name', 'N/A')}")
            cl2.markdown(f"**Designation:** {row.get('lead_researcher_designation', 'N/A')}")

            st.markdown("---")

            # ── Dates ──
            st.markdown("**Timeline**")
            cd1, cd2, cd3 = st.columns(3)
            cd1.markdown(f"**Start Date:** {row.get('start_date', 'N/A')}")
            cd2.markdown(f"**Expected End:** {row.get('expected_end_date', 'N/A')}")
            actual = row.get('actual_end_date')
            cd3.markdown(
                f"**Actual End:** {actual if actual else '—  Not yet completed'}"
            )

            st.markdown("---")

            # ── Budget ──
            if row.get("budget_allocated"):
                utilized = row.get("budget_utilized") or 0
                pct = utilized / row["budget_allocated"] * 100
                st.markdown("**Budget**")
                cb1, cb2, cb3 = st.columns(3)
                cb1.markdown(f"**Allocated:** ₦{row['budget_allocated']:,.0f}")
                cb2.markdown(f"**Utilized:** ₦{utilized:,.0f}")
                cb3.markdown(f"**Utilization:** {pct:.1f}%")
                st.progress(min(pct / 100, 1.0))

            st.markdown("---")
            # Documents section
            st.markdown("---")
            st.markdown("**Project Documents**")
            try:
                proj_docs = fetch_project_documents(row["id"])
                if not proj_docs:
                    st.caption("No documents uploaded for this project.")
                else:
                    for doc in proj_docs:
                        col_doc1, col_doc2 = st.columns([3, 1])
                        col_doc1.markdown(
                            f"📄 {doc['file_name']} — "
                            f"_{doc['document_category']}_"
                        )
                        if col_doc2.button(
                            "Download",
                            key=f"proj_dl_{doc['id']}"
                        ):
                            try:
                                url = get_document_url(doc["storage_path"])
                                st.markdown(
                                    f"[Download {doc['file_name']}]({url})"
                                )
                            except Exception as e:
                                st.error(f"Could not generate link: {e}")
            except Exception:
                st.caption("Documents unavailable.")
            # ── Other details ──
            if row.get("funding_source"):
                st.markdown(f"**Funding Source:** {row['funding_source']}")
            if row.get("summary"):
                st.markdown(f"**Summary:** {row['summary']}")
            if row.get("keywords"):
                st.markdown(f"**Keywords:** `{row['keywords']}`")


# ══════════════════════════════════════════════════════════════════════════
# PAGE 3 — PROTOTYPE TRACKER
# ══════════════════════════════════════════════════════════════════════════
elif page == "Prototype Tracker":
    st.markdown('<div class="page-title">Prototype Development Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Track every prototype from design to commercialization</div>', unsafe_allow_html=True)

    if prototypes_df.empty:
        st.info("No prototypes in the database yet. Add one via Data Entry.")
        st.stop()

    STAGES = ["Design", "Fabrication", "Testing", "Modification",
              "Certification", "Commercialization", "Deployed"]

    for stage in STAGES:
        stage_protos = prototypes_df[prototypes_df["development_stage"] == stage]
        count = len(stage_protos)
        color = "#2E7D32" if count > 0 else "#E0E0E0"

        st.markdown(f"""
        <div style="
            background: white;
            border-left: 5px solid {color};
            border-radius: 8px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 0.6rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        ">
            <span style="color:{color}; font-weight:700; font-size:1rem;">
                {stage}
            </span>
            <span style="
                background:{color};
                color:white;
                border-radius:12px;
                padding:0.1rem 0.6rem;
                font-size:0.78rem;
                margin-left:0.8rem;
                font-weight:600;
            ">{count}</span>
        </div>
        """, unsafe_allow_html=True)

        if count > 0:
            for _, proto in stage_protos.iterrows():
                st.markdown(f"""
                <div style="
                    margin-left:2rem;
                    background:#F1F8E9;
                    border-radius:6px;
                    padding:0.6rem 1rem;
                    margin-bottom:0.4rem;
                    font-size:0.88rem;
                ">
                    🔧 <strong>{proto['name']}</strong> —
                    Crop: {proto.get('target_crop','N/A')} |
                    Region: {proto.get('target_region','N/A')} |
                    Units Produced: {proto.get('units_produced',0)} |
                    Units Distributed: {proto.get('units_distributed',0)}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Stage Distribution</div>', unsafe_allow_html=True)
    stage_counts = prototypes_df["development_stage"].value_counts().reset_index()
    stage_counts.columns = ["Stage", "Count"]
    fig_stages = px.funnel(
        stage_counts,
        x="Count",
        y="Stage",
        color_discrete_sequence=["#2E7D32"]
    )
    fig_stages.update_layout(paper_bgcolor="white", margin=dict(t=10))
    st.plotly_chart(fig_stages, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 4 — RESEARCHERS
# ══════════════════════════════════════════════════════════════════════════
elif page == "Researchers":
    st.markdown(
        '<div class="page-title">Researchers & Staff</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-sub">Research officers, engineers and staff directory</div>',
        unsafe_allow_html=True
    )

    if researchers_df.empty:
        st.info("No researchers in the database yet. Add one via Data Entry.")
        st.stop()

    dept_filter = st.selectbox(
        "Filter by Department", ["All"] + list(DEPT_MAP.values())
    )
    filtered_r = researchers_df.copy()
    if dept_filter != "All":
        dept_id = [k for k, v in DEPT_MAP.items() if v == dept_filter]
        if dept_id:
            filtered_r = filtered_r[
                filtered_r["department_id"] == dept_id[0]
            ]

    for _, r in filtered_r.iterrows():
        with st.expander(
            f"👤 {r['full_name']} — {r.get('designation', 'N/A')}"
        ):
            c1, c2 = st.columns(2)
            c1.markdown(
                f"**Department:** {DEPT_FULL.get(r['department_id'], 'N/A')}"
            )
            c2.markdown(
                f"**Specialization:** {r.get('specialization', 'N/A')}"
            )

            st.markdown("**Contact Details**")
            cc1, cc2 = st.columns(2)
            cc1.markdown(
                f"**Email:** {r.get('email', 'N/A') or 'N/A'}"
            )
            cc2.markdown(
                f"**Phone:** {r.get('phone', 'N/A') or 'N/A'}"
            )

            if any([
                r.get("linkedin"),
                r.get("researchgate"),
                r.get("other_handle")
            ]):
                st.markdown("**Professional Handles**")
                if r.get("linkedin"):
                    st.markdown(f"🔗 LinkedIn: {r['linkedin']}")
                if r.get("researchgate"):
                    st.markdown(f"🔬 ResearchGate: {r['researchgate']}")
                if r.get("other_handle"):
                    st.markdown(f"🌐 Other: {r['other_handle']}")

            status = "Active" if r.get("is_active") else "Inactive"
            st.markdown(f"**Status:** {status}")


# ══════════════════════════════════════════════════════════════════════════
# PAGE 5 — DATA ENTRY (Staff only)
# ══════════════════════════════════════════════════════════════════════════
elif page == "Data Entry":
    st.markdown('<div class="page-title">Data Entry</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Enter and update research records for your department</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ New Project",
        "👤 New Researcher",
        "🎯 New Milestone",
        "🔧 New Prototype",
        "📄 Upload Document"
    ])

    # ── NEW PROJECT ──
    with tab1:
        st.markdown(
            '<div class="section-header">Register a New Project</div>',
            unsafe_allow_html=True
        )
        with st.form("project_form"):
            title = st.text_input("Project Title *")
            dept_options = {v: k for k, v in DEPT_FULL.items()}
            dept_selected = st.selectbox("Department *", list(DEPT_FULL.values()))
            dept_id = dept_options[dept_selected]
            status = st.selectbox("Status *", [
                "Ongoing", "Completed", "Abandoned",
                "Pending Evaluation", "Behind Schedule", "Commercialized"
            ])

            st.markdown("**Principal Supervisor**")
            ps1, ps2 = st.columns(2)
            supervisor_name = ps1.text_input("Supervisor Full Name")
            supervisor_designation = ps2.text_input("Supervisor Designation")
            ps3, ps4 = st.columns(2)
            supervisor_email = ps3.text_input("Supervisor Email")
            supervisor_phone = ps4.text_input("Supervisor Phone")

            st.markdown("**Lead Researcher**")
            lr1, lr2 = st.columns(2)
            lead_researcher_name = lr1.text_input("Lead Researcher Full Name")
            lead_researcher_designation = lr2.text_input("Lead Researcher Designation")

            st.markdown("**Timeline**")
            d1, d2, d3 = st.columns(3)
            start_date = d1.date_input("Start Date")
            expected_end_date = d2.date_input("Expected End Date")
            actual_end_date = d3.date_input(
                "Actual End Date (if completed)",
                value=None
            )

            st.markdown("**Budget**")
            b1, b2 = st.columns(2)
            budget_allocated = b1.number_input(
                "Budget Allocated (₦)", min_value=0.0, step=10000.0
            )
            budget_utilized = b2.number_input(
                "Budget Utilized (₦)", min_value=0.0, step=10000.0
            )

            funding_source = st.text_input("Funding Source")
            objectives = st.text_area("Objectives")
            summary_text = st.text_area("Project Summary")
            keywords = st.text_input("Keywords (comma-separated)")

            machine_built = st.radio(
                "Has a machine/prototype been built from this project?",
                ["No", "Yes"],
                horizontal=True
            )

            submitted = st.form_submit_button("Save Project")
            if submitted:
                if not title:
                    st.error("Project title is required.")
                else:
                    try:
                        add_project({
                            "title": title,
                            "department_id": dept_id,
                            "status": status,
                            "supervisor_name": supervisor_name or None,
                            "supervisor_designation": supervisor_designation or None,
                            "supervisor_email": supervisor_email or None,
                            "supervisor_phone": supervisor_phone or None,
                            "lead_researcher_name": lead_researcher_name or None,
                            "lead_researcher_designation": lead_researcher_designation or None,
                            "start_date": start_date,
                            "expected_end_date": expected_end_date,
                            "actual_end_date": actual_end_date,
                            "budget_allocated": budget_allocated or None,
                            "budget_utilized": budget_utilized or None,
                            "funding_source": funding_source or None,
                            "objectives": objectives or None,
                            "summary": summary_text or None,
                            "keywords": keywords or None,
                            "machine_built": machine_built == "Yes",
                        })
                        st.success("✅ Project saved successfully.")
                    except Exception as e:
                        st.error(f"Error saving project: {e}")

    # ── NEW RESEARCHER ──
    with tab2:
        st.markdown('<div class="section-header">Register a New Researcher</div>', unsafe_allow_html=True)
        with st.form("researcher_form"):
            full_name = st.text_input("Full Name *")
            designation = st.text_input("Designation (e.g. Principal Research Officer)")
            dept_selected_r = st.selectbox("Department *", list(DEPT_FULL.values()), key="rdept")
            dept_id_r = dept_options[dept_selected_r]
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            st.markdown("**Professional Handles**")
            h1, h2, h3 = st.columns(3)
            linkedin = h1.text_input("LinkedIn URL")
            researchgate = h2.text_input("ResearchGate URL")
            other_handle = h3.text_input("Other Handle")
            specialization = st.text_input("Area of Specialization")

            submitted_r = st.form_submit_button("Save Researcher")
            if submitted_r:
                if not full_name:
                    st.error("Full name is required.")
                else:
                    try:
                        add_researcher({
                            "full_name": full_name,
                            "designation": designation or None,
                            "department_id": dept_id_r,
                            "email": email or None,
                            "phone": phone or None,
                            "linkedin": linkedin or None,
                            "researchgate": researchgate or None,
                            "other_handle": other_handle or None,
                            "specialization": specialization or None,
                            "is_active": True
                        })
                        st.success("✅ Researcher saved successfully.")
                    except Exception as e:
                        st.error(f"Error saving researcher: {e}")

    # ── NEW MILESTONE ──
    with tab3:
        st.markdown('<div class="section-header">Add a Project Milestone</div>', unsafe_allow_html=True)
        with st.form("milestone_form"):
            project_options = {
                p["title"][:60]: p["id"] for p in projects
            }
            selected_project = st.selectbox("Select Project *", list(project_options.keys()))
            project_id_m = project_options.get(selected_project)

            m_title = st.text_input("Milestone Title *")
            m_description = st.text_area("Description")
            c1, c2 = st.columns(2)
            due_date = c1.date_input("Due Date")
            completion_date = c2.date_input("Completion Date (if done)", value=None)
            m_status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "Overdue"])

            submitted_m = st.form_submit_button("Save Milestone")
            if submitted_m:
                if not m_title:
                    st.error("Milestone title is required.")
                else:
                    try:
                        add_milestone({
                            "project_id": project_id_m,
                            "title": m_title,
                            "description": m_description or None,
                            "due_date": due_date,
                            "completion_date": completion_date,
                            "status": m_status
                        })
                        st.success("✅ Milestone saved successfully.")
                    except Exception as e:
                        st.error(f"Error saving milestone: {e}")

    # ── NEW PROTOTYPE ──
    with tab4:
        st.markdown('<div class="section-header">Register a New Prototype</div>', unsafe_allow_html=True)
        with st.form("prototype_form"):
            selected_project_p = st.selectbox(
                "Select Project *",
                list(project_options.keys()),
                key="pproject"
            )
            project_id_p = project_options.get(selected_project_p)

            p_name = st.text_input("Prototype Name *")
            p_description = st.text_area("Description")
            p_stage = st.selectbox("Development Stage *", [
                "Design", "Fabrication", "Testing",
                "Modification", "Certification", "Commercialization", "Deployed"
            ])
            stage_start = st.date_input("Stage Start Date")
            c1, c2 = st.columns(2)
            units_produced = c1.number_input("Units Produced", min_value=0, step=1)
            units_distributed = c2.number_input("Units Distributed", min_value=0, step=1)
            target_crop = st.text_input("Target Crop(s)")
            target_region = st.text_input("Target Region")
            p_notes = st.text_area("Notes")

            submitted_p = st.form_submit_button("Save Prototype")
            if submitted_p:
                if not p_name:
                    st.error("Prototype name is required.")
                else:
                    try:
                        add_prototype({
                            "project_id": project_id_p,
                            "name": p_name,
                            "description": p_description or None,
                            "development_stage": p_stage,
                            "stage_start_date": stage_start,
                            "units_produced": units_produced,
                            "units_distributed": units_distributed,
                            "target_crop": target_crop or None,
                            "target_region": target_region or None,
                            "notes": p_notes or None
                        })
                        st.success("✅ Prototype saved successfully.")
                    except Exception as e:
                        st.error(f"Error saving prototype: {e}")


    # ── UPLOAD DOCUMENT ───────────────────────────────────────────────────
    with tab5:
        st.markdown(
            '<div class="section-header">Upload Document</div>',
            unsafe_allow_html=True
        )

        record_type_choice = st.radio(
            "This document belongs to *",
            ["Project", "Research"],
            horizontal=True
        )

        if record_type_choice == "Project":
            link_options = {
                f"[{p['id']}] {p['title'][:60]}": p['id']
                for p in projects
            } if projects else {}
            link_label = "Select Project"
        else:
            link_options = {
                f"[{r['id']}] {r['title'][:60]}": r['id']
                for r in research
            } if research else {}
            link_label = "Select Research Record"

        if not link_options:
            st.info(
                f"No {record_type_choice.lower()} records available. "
                f"Add one via the other tabs first, then upload here."
            )
            st.stop()

        selected_link = st.selectbox(link_label, list(link_options.keys()))
        linked_id = link_options[selected_link]
        project_id_doc = (
            linked_id if record_type_choice == "Project" else None
        )

        doc_category = st.selectbox(
            "Document Category *",
            [
                "Research Paper",
                "Technical Report",
                "Project Proposal",
                "Design Drawing",
                "Prototype Diagram",
                "Testing Report",
                "Commercialization Record",
                "Extension Report",
                "Scanned Document",
                "Other"
            ]
        )

        doc_description = st.text_area(
            "Description",
            placeholder="Brief description of what this document contains..."
        )

        uploaded_by = st.text_input(
            "Uploaded By",
            placeholder="Your name"
        )

        uploaded_file = st.file_uploader(
            "Select File *",
            type=[
                "pdf", "docx", "doc", "xlsx", "xls",
                "png", "jpg", "jpeg", "dwg", "dxf"
            ],
            help="Accepted: PDF, Word, Excel, Images, CAD files"
        )

        if uploaded_file is not None:
            st.markdown(f"""
            <div style="
                background:#F1F8E9;
                border-left:4px solid #4CAF50;
                border-radius:6px;
                padding:0.6rem 1rem;
                font-size:0.85rem;
                color:#1B5E20;
            ">
                📄 <strong>{uploaded_file.name}</strong> —
                {round(uploaded_file.size / 1024, 1)} KB
            </div>
            """, unsafe_allow_html=True)



        if st.button("Upload & Extract", use_container_width=True):
            if not uploaded_file:
                st.error("Please select a file to upload.")
            elif not record_type_choice:
                st.error("Please select whether this is a Project or Research document.")
            else:
                with st.spinner("Uploading and extracting..."):
                    try:
                        file_bytes = uploaded_file.read()

                        # Upload to storage
                        storage_path = upload_document(
                            file_bytes=file_bytes,
                            file_name=uploaded_file.name,
                            project_id=linked_id,
                            category=doc_category.replace(" ", "_")
                        )

                        # Save document record
                        doc_id = save_document_record({
                            "project_id": linked_id
                            if record_type_choice == "Project" else None,
                            "research_id": linked_id
                            if record_type_choice == "Research" else None,
                            "record_type": record_type_choice.lower(),
                            "file_name": uploaded_file.name,
                            "file_type": uploaded_file.type,
                            "document_category": doc_category,
                            "description": doc_description or None,
                            "storage_path": storage_path,
                            "uploaded_by": uploaded_by or None
                        })

                        st.success(f"✅ {uploaded_file.name} uploaded.")

                        # Only extract for PDF and DOCX
                        ext = uploaded_file.name.lower().split(".")[-1]
                        if ext in ["pdf", "docx", "doc"]:
                            st.info("🤖 Extracting research details...")
                            extracted = extract_research_details(
                                file_bytes, uploaded_file.name
                            )

                            if "error" in extracted:
                                st.warning(
                                    f"Extraction issue: {extracted['error']}. "
                                    f"You can add this record manually."
                                )
                            else:
                                save_staging({
                                    "document_id": doc_id,
                                    "extracted_title": extracted.get("title"),
                                    "extracted_lead_researcher": extracted.get(
                                        "lead_researcher"
                                    ),
                                    "extracted_supervisor": extracted.get(
                                        "supervisor"
                                    ),
                                    "extracted_keywords": extracted.get("keywords"),
                                    "extracted_summary": extracted.get("summary"),
                                    "extracted_objectives": extracted.get(
                                        "objectives"
                                    ),
                                    "extracted_findings": extracted.get("findings"),
                                    "extracted_funding_source": extracted.get(
                                        "funding_source"
                                    ),
                                    "extracted_journal": extracted.get("journal_name"),
                                    "extracted_research_type": extracted.get(
                                        "research_type"
                                    ),
                                    "raw_extraction": extracted.get(
                                        "raw_extraction", ""
                                    ),
                                    "submitted_by": uploaded_by or None,
                                    "status": "Pending Confirmation"
                                })
                                st.success(
                                    "🤖 Extraction complete. "
                                    "Go to **Pending Approvals** to review "
                                    "and confirm the extracted details."
                                )
                        else:
                            st.info(
                                "File uploaded. "
                                "AI extraction is only available for PDF and DOCX files."
                            )

                    except Exception as e:
                        st.error(f"Error: {e}")

        # ── VIEW EXISTING DOCUMENTS ───────────────────────────────────────
        st.markdown("---")
        st.markdown(
            '<div class="section-header">Documents for This Project</div>',
            unsafe_allow_html=True
        )

        try:
            existing_docs = fetch_project_documents(project_id_doc)
            if not existing_docs:
                st.info("No documents uploaded for this project yet.")
            else:
                for doc in existing_docs:
                    with st.expander(
                        f"📄 {doc['file_name']} — {doc['document_category']}"
                    ):
                        dc1, dc2 = st.columns(2)
                        dc1.markdown(
                            f"**Category:** {doc['document_category']}"
                        )
                        dc2.markdown(
                            f"**Uploaded by:** {doc.get('uploaded_by', 'N/A')}"
                        )
                        if doc.get("description"):
                            st.markdown(
                                f"**Description:** {doc['description']}"
                            )
                        st.markdown(
                            f"**Uploaded at:** {doc.get('uploaded_at', 'N/A')}"
                        )
                        if st.button(
                            "Generate Download Link",
                            key=f"dl_{doc['id']}"
                        ):
                            try:
                                url = get_document_url(doc["storage_path"])
                                st.markdown(
                                    f"[Click here to download {doc['file_name']}]({url})"
                                )
                                st.caption(
                                    "Link expires in 60 minutes."
                                )
                            except Exception as e:
                                st.error(f"Could not generate link: {e}")
        except Exception as e:
            st.error(f"Could not load documents: {e}")


# ══════════════════════════════════════════════════════════════════════════
# PAGE — UPDATE RECORDS
# ══════════════════════════════════════════════════════════════════════════
elif page == "Update Records":
    st.markdown(
        '<div class="page-title">Update Records</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-sub">'
        'Search and update existing projects, researchers, and prototypes.'
        '</div>',
        unsafe_allow_html=True
    )

    update_tab1, update_tab2, update_tab3 = st.tabs([
        "✏️ Update Project",
        "✏️ Update Researcher",
        "✏️ Update Prototype"
    ])

    # ── UPDATE PROJECT ────────────────────────────────────────────────
    with update_tab1:
        project_options_u = {
            f"[{p['id']}] {p['title'][:60]}": p['id']
            for p in projects
        }
        selected_u = st.selectbox(
            "Select Project to Update",
            list(project_options_u.keys())
        )
        project_id_u = project_options_u.get(selected_u)
        existing = next(
            (p for p in projects if p["id"] == project_id_u), None
        )

        if existing:
            with st.form("update_project_form"):
                title_u = st.text_input(
                    "Project Title", value=existing.get("title", "")
                )
                dept_options_u = {v: k for k, v in DEPT_FULL.items()}
                current_dept = DEPT_FULL.get(
                    existing.get("department_id"), list(DEPT_FULL.values())[0]
                )
                dept_selected_u = st.selectbox(
                    "Department",
                    list(DEPT_FULL.values()),
                    index=list(DEPT_FULL.values()).index(current_dept)
                )
                dept_id_u = dept_options_u[dept_selected_u]

                status_options = [
                    "Ongoing", "Completed", "Abandoned",
                    "Pending Evaluation", "Behind Schedule", "Commercialized"
                ]
                current_status = existing.get("status", "Ongoing")
                status_u = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(current_status)
                    if current_status in status_options else 0
                )

                st.markdown("**Principal Supervisor**")
                us1, us2 = st.columns(2)
                sup_name_u = us1.text_input(
                    "Supervisor Name",
                    value=existing.get("supervisor_name", "") or ""
                )
                sup_desig_u = us2.text_input(
                    "Supervisor Designation",
                    value=existing.get("supervisor_designation", "") or ""
                )
                us3, us4 = st.columns(2)
                sup_email_u = us3.text_input(
                    "Supervisor Email",
                    value=existing.get("supervisor_email", "") or ""
                )
                sup_phone_u = us4.text_input(
                    "Supervisor Phone",
                    value=existing.get("supervisor_phone", "") or ""
                )

                st.markdown("**Lead Researcher**")
                ul1, ul2 = st.columns(2)
                lead_name_u = ul1.text_input(
                    "Lead Researcher Name",
                    value=existing.get("lead_researcher_name", "") or ""
                )
                lead_desig_u = ul2.text_input(
                    "Lead Researcher Designation",
                    value=existing.get("lead_researcher_designation", "") or ""
                )

                st.markdown("**Timeline**")
                ud1, ud2, ud3 = st.columns(3)
                start_u = ud1.date_input(
                    "Start Date",
                    value=existing.get("start_date") or date.today()
                )
                end_u = ud2.date_input(
                    "Expected End Date",
                    value=existing.get("expected_end_date") or date.today()
                )
                actual_u = ud3.date_input(
                    "Actual End Date",
                    value=existing.get("actual_end_date") or None
                )

                st.markdown("**Budget**")
                ub1, ub2 = st.columns(2)
                budget_alloc_u = ub1.number_input(
                    "Budget Allocated (₦)",
                    value=float(existing.get("budget_allocated") or 0),
                    step=10000.0
                )
                budget_util_u = ub2.number_input(
                    "Budget Utilized (₦)",
                    value=float(existing.get("budget_utilized") or 0),
                    step=10000.0
                )

                funding_u = st.text_input(
                    "Funding Source",
                    value=existing.get("funding_source", "") or ""
                )
                objectives_u = st.text_area(
                    "Objectives",
                    value=existing.get("objectives", "") or ""
                )
                summary_u = st.text_area(
                    "Summary",
                    value=existing.get("summary", "") or ""
                )
                keywords_u = st.text_input(
                    "Keywords",
                    value=existing.get("keywords", "") or ""
                )
                machine_u = st.radio(
                    "Machine Built?",
                    ["No", "Yes"],
                    index=1 if existing.get("machine_built") else 0,
                    horizontal=True
                )

                save_u = st.form_submit_button("Save Changes")
                if save_u:
                    try:
                        from database import SessionLocal
                        from models.models import Project as ProjectModel
                        db = SessionLocal()
                        proj = db.query(ProjectModel).filter(
                            ProjectModel.id == project_id_u
                        ).first()
                        if proj:
                            proj.title = title_u
                            proj.department_id = dept_id_u
                            proj.status = status_u
                            proj.supervisor_name = sup_name_u or None
                            proj.supervisor_designation = sup_desig_u or None
                            proj.supervisor_email = sup_email_u or None
                            proj.supervisor_phone = sup_phone_u or None
                            proj.lead_researcher_name = lead_name_u or None
                            proj.lead_researcher_designation = lead_desig_u or None
                            proj.start_date = start_u
                            proj.expected_end_date = end_u
                            proj.actual_end_date = actual_u
                            proj.budget_allocated = budget_alloc_u or None
                            proj.budget_utilized = budget_util_u or None
                            proj.funding_source = funding_u or None
                            proj.objectives = objectives_u or None
                            proj.summary = summary_u or None
                            proj.keywords = keywords_u or None
                            proj.machine_built = machine_u == "Yes"
                            db.commit()
                            st.success("✅ Project updated successfully.")
                        db.close()
                    except Exception as e:
                        st.error(f"Error updating project: {e}")

    # ── UPDATE RESEARCHER ─────────────────────────────────────────────
    with update_tab2:
        researcher_options_u = {
            f"[{r['id']}] {r['full_name']}": r['id']
            for r in researchers
        }
        selected_ru = st.selectbox(
            "Select Researcher to Update",
            list(researcher_options_u.keys())
        )
        researcher_id_u = researcher_options_u.get(selected_ru)
        existing_r = next(
            (r for r in researchers if r["id"] == researcher_id_u), None
        )

        if existing_r:
            with st.form("update_researcher_form"):
                name_ru = st.text_input(
                    "Full Name",
                    value=existing_r.get("full_name", "")
                )
                desig_ru = st.text_input(
                    "Designation",
                    value=existing_r.get("designation", "") or ""
                )
                dept_r_u = st.selectbox(
                    "Department",
                    list(DEPT_FULL.values()),
                    index=max(
                        0,
                        list(DEPT_FULL.keys()).index(
                            existing_r.get("department_id", 1)
                        )
                        if existing_r.get("department_id") in DEPT_FULL
                        else 0
                    )
                )
                dept_id_ru = {v: k for k, v in DEPT_FULL.items()}[dept_r_u]
                spec_ru = st.text_input(
                    "Specialization",
                    value=existing_r.get("specialization", "") or ""
                )
                rc1, rc2 = st.columns(2)
                email_ru = rc1.text_input(
                    "Email",
                    value=existing_r.get("email", "") or ""
                )
                phone_ru = rc2.text_input(
                    "Phone",
                    value=existing_r.get("phone", "") or ""
                )
                rh1, rh2, rh3 = st.columns(3)
                linkedin_ru = rh1.text_input(
                    "LinkedIn",
                    value=existing_r.get("linkedin", "") or ""
                )
                rg_ru = rh2.text_input(
                    "ResearchGate",
                    value=existing_r.get("researchgate", "") or ""
                )
                other_ru = rh3.text_input(
                    "Other Handle",
                    value=existing_r.get("other_handle", "") or ""
                )
                active_ru = st.radio(
                    "Status",
                    ["Active", "Inactive"],
                    index=0 if existing_r.get("is_active") else 1,
                    horizontal=True
                )

                save_ru = st.form_submit_button("Save Changes")
                if save_ru:
                    try:
                        from database import SessionLocal
                        from models.models import Researcher as ResearcherModel
                        db = SessionLocal()
                        researcher = db.query(ResearcherModel).filter(
                            ResearcherModel.id == researcher_id_u
                        ).first()
                        if researcher:
                            researcher.full_name = name_ru
                            researcher.designation = desig_ru or None
                            researcher.department_id = dept_id_ru
                            researcher.specialization = spec_ru or None
                            researcher.email = email_ru or None
                            researcher.phone = phone_ru or None
                            researcher.linkedin = linkedin_ru or None
                            researcher.researchgate = rg_ru or None
                            researcher.other_handle = other_ru or None
                            researcher.is_active = active_ru == "Active"
                            db.commit()
                            st.success("✅ Researcher updated successfully.")
                        db.close()
                    except Exception as e:
                        st.error(f"Error updating researcher: {e}")

    # ── UPDATE PROTOTYPE ──────────────────────────────────────────────
    with update_tab3:
        if prototypes:
            proto_options_u = {
                f"[{p['id']}] {p['name']}": p['id']
                for p in prototypes
            }
            selected_pu = st.selectbox(
                "Select Prototype to Update",
                list(proto_options_u.keys())
            )
            proto_id_u = proto_options_u[selected_pu]
            existing_p = next(
                (p for p in prototypes if p["id"] == proto_id_u), None
            )

            if existing_p:
                with st.form("update_prototype_form"):
                    pname_u = st.text_input(
                        "Prototype Name",
                        value=existing_p.get("name", "")
                    )
                    pdesc_u = st.text_area(
                        "Description",
                        value=existing_p.get("description", "") or ""
                    )
                    stage_options = [
                        "Design", "Fabrication", "Testing",
                        "Modification", "Certification",
                        "Commercialization", "Deployed"
                    ]
                    current_stage = existing_p.get("development_stage", "Design")
                    pstage_u = st.selectbox(
                        "Development Stage",
                        stage_options,
                        index=stage_options.index(current_stage)
                        if current_stage in stage_options else 0
                    )
                    pp1, pp2 = st.columns(2)
                    units_prod_u = pp1.number_input(
                        "Units Produced",
                        value=int(existing_p.get("units_produced") or 0),
                        min_value=0
                    )
                    units_dist_u = pp2.number_input(
                        "Units Distributed",
                        value=int(existing_p.get("units_distributed") or 0),
                        min_value=0
                    )
                    crop_u = st.text_input(
                        "Target Crop(s)",
                        value=existing_p.get("target_crop", "") or ""
                    )
                    region_u = st.text_input(
                        "Target Region",
                        value=existing_p.get("target_region", "") or ""
                    )
                    notes_u = st.text_area(
                        "Notes",
                        value=existing_p.get("notes", "") or ""
                    )

                    save_pu = st.form_submit_button("Save Changes")
                    if save_pu:
                        try:
                            from database import SessionLocal
                            from models.models import Prototype as ProtoModel
                            db = SessionLocal()
                            proto = db.query(ProtoModel).filter(
                                ProtoModel.id == proto_id_u
                            ).first()
                            if proto:
                                proto.name = pname_u
                                proto.description = pdesc_u or None
                                proto.development_stage = pstage_u
                                proto.units_produced = units_prod_u
                                proto.units_distributed = units_dist_u
                                proto.target_crop = crop_u or None
                                proto.target_region = region_u or None
                                proto.notes = notes_u or None
                                db.commit()
                                st.success(
                                    "✅ Prototype updated successfully."
                                )
                            db.close()
                        except Exception as e:
                            st.error(f"Error updating prototype: {e}")
        else:
            st.info(
                "No prototypes in the database yet. "
                "Add one through Data Entry first."
            )



# ══════════════════════════════════════════════════════════════════════════
# PAGE 6 — AI SEARCH
# ══════════════════════════════════════════════════════════════════════════
elif page == "AI Search":
    st.markdown('<div class="page-title">Research Intelligence Search</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Ask a question in plain English — '
        'the system searches the project database and returns a direct answer.</div>',
        unsafe_allow_html=True
    )

    # ── Example queries ──
    st.markdown('<div class="section-header">Example Questions</div>',
                unsafe_allow_html=True)

    examples = [
        "Which projects are currently behind schedule?",
        "Show me all completed FPM projects.",
        "Which prototypes have reached the testing stage?",
        "What projects are funded by FMARD?",
        "Which projects have utilized more than 90% of their budget?",
        "List all ongoing projects in Engineering and Scientific Services.",
    ]

    cols = st.columns(3)
    for i, example in enumerate(examples):
        with cols[i % 3]:
            if st.button(example, key=f"example_{i}"):
                st.session_state["search_query"] = example

    st.markdown("---")

    # ── Search input ──
    query = st.text_input(
        "Your Question",
        value=st.session_state.get("search_query", ""),
        placeholder="e.g. Which FPM projects are still ongoing?",
        key="search_input"
    )

    col_ai, col_kw = st.columns([1, 1])
    with col_ai:
        search_ai = st.button("🤖 Ask AI", use_container_width=True)
    with col_kw:
        search_kw = st.button("🔍 Keyword Search", use_container_width=True)

    # ── AI Search ──
    all_data = {
        "projects": projects_df,
        "research": research_df,
        "researchers": researchers_df,
        "prototypes": prototypes_df
    }


    if search_ai and query:
        with st.spinner("Searching..."):
            result = ai_search(query, all_data, DEPT_MAP, DEPT_FULL)

        if result["mode"] == "ai":
            st.success("🤖 AI Answer")
        else:
            st.warning("⚠️ AI unavailable — showing keyword results.")

        st.markdown(f"""
        <div style="
            background: #F1F8E9;
            border-left: 4px solid #4CAF50;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
            font-size: 0.95rem;
            color: #1B5E20;
            line-height: 1.7;
        ">
            {result['answer']}
        </div>
        """, unsafe_allow_html=True)

        # Matched records are rendered from result["matched"] below.

        
        matched = result.get("matched", {}) or {}
        if not any(matched.values()):
            st.info("No matching records found for this query.")
        else:
            for record_type, ids in result["matched"].items():
                if not ids:
                    continue
                st.markdown(
                    f'<div class="section-header">'
                    f'{record_type.title()} ({len(ids)})'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if record_type == "projects" and not projects_df.empty:
                    matched_df = projects_df[
                        projects_df["id"].isin(ids)
                    ].copy()
                    matched_df["Department"] = matched_df[
                        "department_id"
                    ].map(DEPT_FULL)
                    for _, proj in matched_df.iterrows():
                        with st.expander(f"📋 {proj['title']}"):
                            c1, c2, c3 = st.columns(3)
                            c1.markdown(
                                f"**Dept:** {proj.get('Department','N/A')}"
                            )
                            c2.markdown(
                                f"**Status:** {proj.get('status','N/A')}"
                            )
                            c3.markdown(
                                f"**Lead:** "
                                f"{proj.get('lead_researcher_name','N/A')}"
                            )

                elif record_type == "research" and not research_df.empty:
                    matched_df = research_df[
                        research_df["id"].isin(ids)
                    ].copy()
                    matched_df["Department"] = matched_df[
                        "department_id"
                    ].map(DEPT_FULL)
                    for _, res in matched_df.iterrows():
                        with st.expander(f"🔬 {res['title']}"):
                            c1, c2, c3 = st.columns(3)
                            c1.markdown(
                                f"**Type:** {res.get('research_type','N/A')}"
                            )
                            c2.markdown(
                                f"**Status:** {res.get('status','N/A')}"
                            )
                            c3.markdown(
                                f"**Lead:** "
                                f"{res.get('lead_researcher_name','N/A')}"
                            )
                            if res.get("summary"):
                                st.markdown(
                                    f"**Summary:** {res['summary']}"
                                )

                elif record_type == "researchers" and not researchers_df.empty:
                    matched_df = researchers_df[
                        researchers_df["id"].isin(ids)
                    ].copy()
                    for _, r in matched_df.iterrows():
                        with st.expander(f"👤 {r['full_name']}"):
                            c1, c2 = st.columns(2)
                            c1.markdown(
                                f"**Dept:** "
                                f"{DEPT_FULL.get(r['department_id'],'N/A')}"
                            )
                            c2.markdown(
                                f"**Specialization:** "
                                f"{r.get('specialization','N/A')}"
                            )

                elif record_type == "prototypes" and not prototypes_df.empty:
                    matched_df = prototypes_df[
                        prototypes_df["id"].isin(ids)
                    ].copy()
                    for _, p in matched_df.iterrows():
                        with st.expander(f"🔧 {p['name']}"):
                            c1, c2 = st.columns(2)
                            c1.markdown(
                                f"**Stage:** "
                                f"{p.get('development_stage','N/A')}"
                            )
                            c2.markdown(
                                f"**Crop:** "
                                f"{p.get('target_crop','N/A')}"
                            )
        
        if result.get("error"):
            with st.expander("Technical details"):
                st.code(result["error"])

    # ── Keyword Search ──
    if search_kw and query:
        kw_results = keyword_search(query, all_data, DEPT_MAP)
        total_kw = sum(len(v) for v in kw_results.values())

        st.markdown(
            f'<div class="section-header">Keyword Results '
            f'({total_kw})</div>',
            unsafe_allow_html=True
        )

        if not total_kw:
            st.info(f"No records found matching '{query}'.")
        else:
            for record_type, records in kw_results.items():
                if not records:
                    continue
                st.markdown(f"**{record_type.title()} ({len(records)})**")
                df_kw = pd.DataFrame(records)
                if "department_id" in df_kw.columns:
                    df_kw["Department"] = df_kw["department_id"].map(DEPT_FULL)
                st.dataframe(
                    df_kw, use_container_width=True, hide_index=True
                )

    # ── Search Log ──
    if query and (search_ai or search_kw):
        try:
            from database import SessionLocal
            from models.models import SearchLog
            if search_ai:
                results_count = sum(
                    len(v) for v in result.get("matched", {}).values()
                )
            else:
                results_count = sum(len(v) for v in kw_results.values())
            db = SessionLocal()
            log = SearchLog(
                query_text=query,
                queried_by=role,
                results_returned=results_count
            )
            db.add(log)
            db.commit()
            db.close()
        except Exception:
            pass



# ══════════════════════════════════════════════════════════════════════
# PAGE 7 — RESEARCH
# ══════════════════════════════════════════════════════════════════════
elif page == "Research":
    st.markdown(
        '<div class="page-title">Research Records</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-sub">'
        'All research studies, papers, and investigations'
        '</div>',
        unsafe_allow_html=True
    )

    if research_df.empty:
        st.info(
            "No research records yet. "
            "Upload a document to extract and create one, "
            "or use Data Entry to add manually."
        )
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            dept_filter_r = st.selectbox(
                "Filter by Department",
                ["All"] + list(DEPT_MAP.values()),
                key="res_dept"
            )
        with col2:
            status_filter_r = st.selectbox(
                "Filter by Status",
                ["All", "Ongoing", "Completed",
                 "Abandoned", "Pending Review", "Published"],
                key="res_status"
            )
        with col3:
            type_filter = st.selectbox(
                "Filter by Type",
                ["All", "Experimental", "Applied", "Adaptive",
                 "Survey", "Review", "Development",
                 "Evaluation", "Other"],
                key="res_type"
            )

        search_r = st.text_input(
            "Search research",
            placeholder="title, keyword, researcher...",
            key="res_search"
        )

        filtered_r = research_df.copy()
        if dept_filter_r != "All":
            filtered_r = filtered_r[
                filtered_r["department_id"].map(DEPT_MAP) == dept_filter_r
            ]
        if status_filter_r != "All":
            filtered_r = filtered_r[
                filtered_r["status"] == status_filter_r
            ]
        if type_filter != "All":
            filtered_r = filtered_r[
                filtered_r["research_type"] == type_filter
            ]
        if search_r:
            mask = (
                filtered_r["title"].str.lower().str.contains(
                    search_r.lower(), na=False
                ) |
                filtered_r.get(
                    "keywords", pd.Series()
                ).str.lower().str.contains(search_r.lower(), na=False) |
                filtered_r.get(
                    "lead_researcher_name", pd.Series()
                ).str.lower().str.contains(search_r.lower(), na=False)
            )
            filtered_r = filtered_r[mask]

        st.markdown(f"**{len(filtered_r)} record(s) found**")
        st.markdown("---")

        for _, row in filtered_r.iterrows():
            machine_label = (
                "🔧 Machine Built"
                if row.get("machine_built")
                else "📄 No Machine"
            )
            machine_color = (
                "#2E7D32"
                if row.get("machine_built")
                else "#9E9E9E"
            )
            extracted_badge = (
                "<span style='background:#1565C0;color:white;"
                "padding:0.1rem 0.5rem;border-radius:10px;"
                "font-size:0.7rem;margin-left:0.5rem;'>"
                "AI Extracted</span>"
                if row.get("extracted_from_document")
                else ""
            )

            with st.expander(f"🔬 {row['title']}"):
                st.markdown(
                    f"**Type:** {row.get('research_type','N/A')} | "
                    f"**Status:** {row.get('status','N/A')} | "
                    f"<span style='background:{machine_color};"
                    f"color:white;padding:0.15rem 0.6rem;"
                    f"border-radius:10px;font-size:0.75rem;'>"
                    f"{machine_label}</span>{extracted_badge}",
                    unsafe_allow_html=True
                )
                st.markdown("---")

                cs1, cs2 = st.columns(2)
                cs1.markdown("**Principal Supervisor**")
                cs1.markdown(
                    f"Name: {row.get('supervisor_name','N/A')}"
                )
                cs1.markdown(
                    f"Designation: "
                    f"{row.get('supervisor_designation','N/A')}"
                )
                cs1.markdown(
                    f"Email: {row.get('supervisor_email','N/A')}"
                )

                cs2.markdown("**Lead Researcher**")
                cs2.markdown(
                    f"Name: "
                    f"{row.get('lead_researcher_name','N/A')}"
                )
                cs2.markdown(
                    f"Designation: "
                    f"{row.get('lead_researcher_designation','N/A')}"
                )

                st.markdown("---")
                cd1, cd2, cd3 = st.columns(3)
                cd1.markdown(
                    f"**Start:** {row.get('start_date','N/A')}"
                )
                cd2.markdown(
                    f"**Expected End:** "
                    f"{row.get('expected_end_date','N/A')}"
                )
                actual = row.get("actual_end_date")
                cd3.markdown(
                    f"**Actual End:** "
                    f"{actual if actual else '— Not completed'}"
                )

                if row.get("journal_name"):
                    st.markdown(
                        f"**Journal:** {row['journal_name']}"
                    )
                if row.get("doi_or_link"):
                    st.markdown(
                        f"**DOI/Link:** [{row['doi_or_link']}]"
                        f"({row['doi_or_link']})"
                    )
                if row.get("funding_source"):
                    st.markdown(
                        f"**Funding:** {row['funding_source']}"
                    )
                if row.get("summary"):
                    st.markdown(f"**Summary:** {row['summary']}")
                if row.get("findings"):
                    st.markdown(f"**Findings:** {row['findings']}")
                if row.get("keywords"):
                    st.markdown(
                        f"**Keywords:** `{row['keywords']}`"
                    )

                # Documents
                st.markdown("---")
                st.markdown("**Documents**")
                try:
                    docs = fetch_project_documents(row["id"])
                    if not docs:
                        st.caption("No documents uploaded.")
                    else:
                        for doc in docs:
                            dc1, dc2 = st.columns([3, 1])
                            dc1.markdown(
                                f"📄 {doc['file_name']} — "
                                f"_{doc['document_category']}_"
                            )
                            if dc2.button(
                                "Download",
                                key=f"res_dl_{doc['id']}"
                            ):
                                url = get_document_url(
                                    doc["storage_path"]
                                )
                                st.markdown(
                                    f"[Download {doc['file_name']}]"
                                    f"({url})"
                                )
                except Exception:
                    st.caption("Documents unavailable.")



# ══════════════════════════════════════════════════════════════════════
# PAGE — PENDING APPROVALS
# ══════════════════════════════════════════════════════════════════════
elif page == "Pending Approvals":
    st.markdown(
        '<div class="page-title">Pending Approvals</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-sub">'
        'Review and confirm AI-extracted research records '
        'before they are saved to the database.'
        '</div>',
        unsafe_allow_html=True
    )

    pending = fetch_pending_staging()

    if not pending:
        st.success(
            "✅ No pending approvals. All extractions have been reviewed."
        )
    else:
        st.markdown(
            f"**{len(pending)} record(s) awaiting confirmation**"
        )
        st.markdown("---")
        confirmer = st.text_input(
            "Your Name (required to confirm or reject)"
        )

        for record in pending:
            with st.expander(
                f"📄 Extracted: "
                f"{record.get('extracted_title','Untitled')}"
            ):
                st.markdown(
                    "Review the AI-extracted details below. "
                    "Edit anything that needs correcting, "
                    "then confirm to save to the database."
                )

                dept_opts = {v: k for k, v in DEPT_FULL.items()}
                with st.form(f"confirm_form_{record['id']}"):
                    title_c = st.text_input(
                        "Title",
                        value=record.get("extracted_title", "") or ""
                    )
                    dept_c = st.selectbox(
                        "Department",
                        list(DEPT_FULL.values())
                    )
                    dept_id_c = dept_opts[dept_c]

                    type_options = [
                        "Experimental", "Applied", "Adaptive",
                        "Survey", "Review", "Development",
                        "Evaluation", "Other"
                    ]
                    rt = record.get("extracted_research_type", "Other")
                    rtype_c = st.selectbox(
                        "Research Type",
                        type_options,
                        index=type_options.index(rt)
                        if rt in type_options else 7
                    )

                    lead_c = st.text_input(
                        "Lead Researcher",
                        value=record.get(
                            "extracted_lead_researcher", ""
                        ) or ""
                    )
                    sup_c = st.text_input(
                        "Supervisor",
                        value=record.get(
                            "extracted_supervisor", ""
                        ) or ""
                    )
                    kw_c = st.text_input(
                        "Keywords",
                        value=record.get(
                            "extracted_keywords", ""
                        ) or ""
                    )
                    sum_c = st.text_area(
                        "Summary",
                        value=record.get(
                            "extracted_summary", ""
                        ) or ""
                    )
                    obj_c = st.text_area(
                        "Objectives",
                        value=record.get(
                            "extracted_objectives", ""
                        ) or ""
                    )
                    find_c = st.text_area(
                        "Findings",
                        value=record.get(
                            "extracted_findings", ""
                        ) or ""
                    )
                    fund_c = st.text_input(
                        "Funding Source",
                        value=record.get(
                            "extracted_funding_source", ""
                        ) or ""
                    )
                    journal_c = st.text_input(
                        "Journal Name",
                        value=record.get(
                            "extracted_journal", ""
                        ) or ""
                    )
                    machine_c = st.radio(
                        "Machine Built?",
                        ["No", "Yes"],
                        horizontal=True
                    )

                    col_approve, col_reject = st.columns(2)
                    approve = col_approve.form_submit_button(
                        "✅ Confirm & Save",
                        use_container_width=True
                    )
                    reject = col_reject.form_submit_button(
                        "❌ Reject",
                        use_container_width=True
                    )

                    if approve:
                        if not confirmer:
                            st.error(
                                "Please enter your name above "
                                "before confirming."
                            )
                        else:
                            try:
                                confirm_staging(
                                    staging_id=record["id"],
                                    confirmed_by=confirmer,
                                    data={
                                        "title": title_c,
                                        "department_id": dept_id_c,
                                        "research_type": rtype_c,
                                        "lead_researcher_name": lead_c or None,
                                        "supervisor_name": sup_c or None,
                                        "keywords": kw_c or None,
                                        "summary": sum_c or None,
                                        "objectives": obj_c or None,
                                        "findings": find_c or None,
                                        "funding_source": fund_c or None,
                                        "journal_name": journal_c or None,
                                        "machine_built": machine_c == "Yes",
                                        "status": "Completed",
                                        "extracted_from_document": True,
                                        "extraction_confirmed": True,
                                    }
                                )
                                st.success(
                                    f"✅ Research record saved: {title_c}"
                                )
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error saving: {e}")

                    if reject:
                        if not confirmer:
                            st.error("Please enter your name first.")
                        else:
                            try:
                                reject_staging(record["id"])
                                st.warning("Record rejected.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error rejecting: {e}")