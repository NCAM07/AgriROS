import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from PIL import Image
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_search.search import ai_search, keyword_search

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dashboard.utils.db import (
    fetch_summary, fetch_all_projects, fetch_all_departments,
    fetch_all_researchers, fetch_prototypes,
    add_project, add_researcher, add_milestone, add_prototype
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
ncam_logo = Image.open("ncam-logo.png")

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
    try:
        projects = fetch_all_projects()
        if not projects:
            projects = PLACEHOLDER_PROJECTS
            using_placeholder = True
        else:
            using_placeholder = False
        prototypes = fetch_prototypes() or PLACEHOLDER_PROTOTYPES
        researchers = fetch_all_researchers() or PLACEHOLDER_RESEARCHERS
        summary = fetch_summary()
        if summary["total"] == 0:
            summary = {
                "total": len(PLACEHOLDER_PROJECTS),
                "ongoing": sum(1 for p in PLACEHOLDER_PROJECTS if p["status"] == "Ongoing"),
                "completed": sum(1 for p in PLACEHOLDER_PROJECTS if p["status"] == "Completed"),
                "commercialized": sum(1 for p in PLACEHOLDER_PROJECTS if p["status"] == "Commercialized"),
                "pending": sum(1 for p in PLACEHOLDER_PROJECTS if p["status"] == "Pending Evaluation"),
                "behind": sum(1 for p in PLACEHOLDER_PROJECTS if p["status"] == "Behind Schedule"),
                "abandoned": sum(1 for p in PLACEHOLDER_PROJECTS if p["status"] == "Abandoned"),
            }
            using_placeholder = True
        return projects, prototypes, researchers, summary, using_placeholder
    except Exception as e:
        st.error(f"Database connection issue: {e}")
        return (PLACEHOLDER_PROJECTS, PLACEHOLDER_PROTOTYPES,
                PLACEHOLDER_RESEARCHERS,
                {
                    "total": 8, "ongoing": 2, "completed": 2,
                    "commercialized": 1, "pending": 1, "behind": 1, "abandoned": 1
                }, True)


projects, prototypes, researchers, summary, using_placeholder = load_data()
projects_df = pd.DataFrame(projects)
prototypes_df = pd.DataFrame(prototypes)
researchers_df = pd.DataFrame(researchers)


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
        "Prototype Tracker",
        "Researchers",
        "AI Search",
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
    c1.metric("Total Projects", summary["total"])
    c2.metric("Ongoing", summary["ongoing"])
    c3.metric("Completed", summary["completed"])
    c4.metric("Commercialized", summary["commercialized"])
    c5.metric("Pending Evaluation", summary["pending"])
    c6.metric("Behind Schedule", summary["behind"])
    c7.metric("Abandoned", summary["abandoned"])

    st.markdown("---")

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

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ New Project",
        "👤 New Researcher",
        "🎯 New Milestone",
        "🔧 New Prototype"
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
            project_id_m = project_options[selected_project]

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
            project_id_p = project_options[selected_project_p]

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
        project_id_u = project_options_u[selected_u]
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
        researcher_id_u = researcher_options_u[selected_ru]
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
    if search_ai and query:
        with st.spinner("Searching..."):
            result = ai_search(query, projects_df, DEPT_MAP, DEPT_FULL)

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

        if result["matched_ids"]:
            st.markdown(
                f'<div class="section-header">Matched Projects '
                f'({len(result["matched_ids"])})</div>',
                unsafe_allow_html=True
            )
            matched_df = projects_df[
                projects_df["id"].isin(result["matched_ids"])
            ].copy()
            matched_df["Department"] = matched_df["department_id"].map(DEPT_FULL)
            matched_df["Department"] = matched_df["department_id"].map(DEPT_FULL)
            for _, proj in matched_df.iterrows():
                with st.expander(
                    f"📋 {proj['title']} — {proj.get('status', 'N/A')}"
                ):
                    ca, cb, cc = st.columns(3)
                    ca.markdown(
                        f"**Department:** {proj.get('Department', 'N/A')}"
                    )
                    cb.markdown(
                        f"**Status:** {proj.get('status', 'N/A')}"
                    )
                    cc.markdown(
                        f"**Research Lead:** "
                        f"{proj.get('lead_researcher_name', 'N/A')}"
                    )
                    cd, ce, cf = st.columns(3)
                    cd.markdown(
                        f"**Supervisor:** "
                        f"{proj.get('supervisor_name', 'N/A')}"
                    )
                    ce.markdown(
                        f"**Start Date:** {proj.get('start_date', 'N/A')}"
                    )
                    cf.markdown(
                        f"**Expected End:** "
                        f"{proj.get('expected_end_date', 'N/A')}"
                    )
                    if proj.get("summary"):
                        st.markdown(f"**Summary:** {proj['summary']}")
                    if proj.get("keywords"):
                        st.markdown(f"**Keywords:** `{proj['keywords']}`")
        else:
            st.info("No matching projects found for this query.")

        if result.get("error"):
            with st.expander("Technical details"):
                st.code(result["error"])

    # ── Keyword Search ──
    if search_kw and query:
        kw_results = keyword_search(query, projects_df, DEPT_MAP)

        st.markdown(
            f'<div class="section-header">Keyword Results '
            f'({len(kw_results)})</div>',
            unsafe_allow_html=True
        )

        if kw_results.empty:
            st.info(f"No projects found matching '{query}'.")
        else:
            matched_df["Department"] = matched_df["department_id"].map(DEPT_FULL)
            for _, proj in matched_df.iterrows():
                with st.expander(
                    f"📋 {proj['title']} — {proj.get('status', 'N/A')}"
                ):
                    ca, cb, cc = st.columns(3)
                    ca.markdown(
                        f"**Department:** {proj.get('Department', 'N/A')}"
                    )
                    cb.markdown(
                        f"**Status:** {proj.get('status', 'N/A')}"
                    )
                    cc.markdown(
                        f"**Research Lead:** "
                        f"{proj.get('lead_researcher_name', 'N/A')}"
                    )
                    cd, ce, cf = st.columns(3)
                    cd.markdown(
                        f"**Supervisor:** "
                        f"{proj.get('supervisor_name', 'N/A')}"
                    )
                    ce.markdown(
                        f"**Start Date:** {proj.get('start_date', 'N/A')}"
                    )
                    cf.markdown(
                        f"**Expected End:** "
                        f"{proj.get('expected_end_date', 'N/A')}"
                    )
                    if proj.get("summary"):
                        st.markdown(f"**Summary:** {proj['summary']}")
                    if proj.get("keywords"):
                        st.markdown(f"**Keywords:** `{proj['keywords']}`")

    # ── Search Log ──
    if query and (search_ai or search_kw):
        try:
            from database import SessionLocal
            from models.models import SearchLog
            db = SessionLocal()
            log = SearchLog(
                query_text=query,
                queried_by=role,
                results_returned=len(
                    result["matched_ids"]
                    if search_ai
                    else kw_results
                )
            )
            db.add(log)
            db.commit()
            db.close()
        except Exception:
            pass