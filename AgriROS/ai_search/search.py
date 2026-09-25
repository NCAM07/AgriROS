import os
import json
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def keyword_search(
    query: str,
    data: dict,
    dept_map: dict = None
) -> dict:
    """
    Keyword search across all record types.
    data = {
        "projects": projects_df,
        "research": research_df,
        "researchers": researchers_df,
        "prototypes": prototypes_df
    }
    Returns matched records grouped by type.
    """
    q = query.lower()
    results = {}

    # Projects
    if "projects" in data and not data["projects"].empty:
        df = data["projects"].copy()
        mask = (
            df.get("title", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("keywords", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("status", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("funding_source", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("summary", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("lead_researcher_name", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("supervisor_name", pd.Series()).str.lower().str.contains(q, na=False)
        )
        results["projects"] = df[mask].to_dict("records")

    # Research
    if "research" in data and not data["research"].empty:
        df = data["research"].copy()
        mask = (
            df.get("title", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("keywords", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("status", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("summary", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("findings", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("lead_researcher_name", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("research_type", pd.Series()).str.lower().str.contains(q, na=False)
        )
        results["research"] = df[mask].to_dict("records")

    # Researchers
    if "researchers" in data and not data["researchers"].empty:
        df = data["researchers"].copy()
        mask = (
            df.get("full_name", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("specialization", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("designation", pd.Series()).str.lower().str.contains(q, na=False)
        )
        results["researchers"] = df[mask].to_dict("records")

    # Prototypes
    if "prototypes" in data and not data["prototypes"].empty:
        df = data["prototypes"].copy()
        mask = (
            df.get("name", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("development_stage", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("target_crop", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("target_region", pd.Series()).str.lower().str.contains(q, na=False) |
            df.get("notes", pd.Series()).str.lower().str.contains(q, na=False)
        )
        results["prototypes"] = df[mask].to_dict("records")

    return results


def build_full_context(data: dict, dept_full: dict) -> str:
    """
    Builds a text context from all record types
    for the AI to reason over.
    """
    sections = []

    # Projects
    if "projects" in data and not data["projects"].empty:
        df = data["projects"].copy().head(30)
        df["dept"] = df["department_id"].map(dept_full).fillna("Unknown")
        lines = ["=== PROJECTS ==="]
        for _, r in df.iterrows():
            budget = (
                f"₦{r['budget_allocated']:,}"
                if r.get("budget_allocated") is not None
                else "N/A"
            )
            lines.append(
                f"[Project ID {r['id']}] {r['title']} | "
                f"Dept: {r['dept']} | Status: {r.get('status','N/A')} | "
                f"Lead: {r.get('lead_researcher_name','N/A')} | "
                f"Supervisor: {r.get('supervisor_name','N/A')} | "
                f"Budget: {budget} | "
                f"Start: {r.get('start_date','N/A')} | "
                f"End: {r.get('expected_end_date','N/A')} | "
                f"Machine Built: {r.get('machine_built', False)} | "
                f"Keywords: {r.get('keywords','N/A')}"
            )
        sections.append("\n".join(lines))

    # Research
    if "research" in data and not data["research"].empty:
        df = data["research"].copy().head(30)
        df["dept"] = df["department_id"].map(dept_full).fillna("Unknown")
        lines = ["=== RESEARCH ==="]
        for _, r in df.iterrows():
            lines.append(
                f"[Research ID {r['id']}] {r['title']} | "
                f"Dept: {r['dept']} | "
                f"Type: {r.get('research_type','N/A')} | "
                f"Status: {r.get('status','N/A')} | "
                f"Lead: {r.get('lead_researcher_name','N/A')} | "
                f"Supervisor: {r.get('supervisor_name','N/A')} | "
                f"Keywords: {r.get('keywords','N/A')} | "
                f"Journal: {r.get('journal_name','N/A')} | "
                f"Machine Built: {r.get('machine_built',False)} | "
                f"Summary: {str(r.get('summary','N/A'))[:200]}"
            )
        sections.append("\n".join(lines))

    # Researchers
    if "researchers" in data and not data["researchers"].empty:
        df = data["researchers"].copy()
        df["dept"] = df["department_id"].map(dept_full).fillna("Unknown")
        lines = ["=== RESEARCHERS ==="]
        for _, r in df.iterrows():
            lines.append(
                f"[Researcher ID {r['id']}] {r['full_name']} | "
                f"Dept: {r['dept']} | "
                f"Designation: {r.get('designation','N/A')} | "
                f"Specialization: {r.get('specialization','N/A')} | "
                f"Active: {r.get('is_active', True)}"
            )
        sections.append("\n".join(lines))

    # Prototypes
    if "prototypes" in data and not data["prototypes"].empty:
        df = data["prototypes"].copy()
        lines = ["=== PROTOTYPES ==="]
        for _, r in df.iterrows():
            lines.append(
                f"[Prototype ID {r['id']}] {r['name']} | "
                f"Stage: {r.get('development_stage','N/A')} | "
                f"Crop: {r.get('target_crop','N/A')} | "
                f"Region: {r.get('target_region','N/A')} | "
                f"Units Produced: {r.get('units_produced',0)} | "
                f"Units Distributed: {r.get('units_distributed',0)}"
            )
        sections.append("\n".join(lines))

    return "\n\n".join(sections)


def ai_search(
    query: str,
    data: dict,
    dept_map: dict,
    dept_full: dict
) -> dict:
    """
    AI search across all record types.
    Returns answer, matched IDs per type, and mode.
    """
    try:
        context = build_full_context(data, dept_full)

        system_prompt = """You are a research intelligence assistant for the National Centre for Agricultural Mechanization (NCAM) in Nigeria.

You have access to NCAM's complete database including Projects, Research records, Researchers, and Prototypes.

Answer the user's question accurately using only the data provided. Be specific and thorough — include names, IDs, statuses, and relevant details in your answer.

At the end of your response, list matched record IDs in this exact format:
MATCHED_PROJECTS: [1, 2]
MATCHED_RESEARCH: [3]
MATCHED_RESEARCHERS: [1]
MATCHED_PROTOTYPES: [2]

Rules:
- Only use information from the data provided.
- If nothing matches, say so clearly and return empty lists.
- Keep answers clear and well-structured.
- Always include all four MATCHED lines even if empty."""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Database:\n{context}\n\nQuestion: {query}"
                }
            ],
            temperature=0.1,
            max_tokens=800
        )

        raw = response.choices[0].message.content.strip()

        # Parse answer and matched IDs
        answer = raw
        matched = {
            "projects": [],
            "research": [],
            "researchers": [],
            "prototypes": []
        }

        for line in raw.split("\n"):
            line = line.strip()
            if line.startswith("MATCHED_PROJECTS:"):
                answer = raw[:raw.find("MATCHED_PROJECTS:")].strip()
                matched["projects"] = _parse_ids(line)
            elif line.startswith("MATCHED_RESEARCH:"):
                matched["research"] = _parse_ids(line)
            elif line.startswith("MATCHED_RESEARCHERS:"):
                matched["researchers"] = _parse_ids(line)
            elif line.startswith("MATCHED_PROTOTYPES:"):
                matched["prototypes"] = _parse_ids(line)

        return {
            "mode": "ai",
            "answer": answer,
            "matched": matched,
            "error": None
        }

    except Exception as e:
        kw_results = keyword_search(query, data, dept_map)
        total = sum(len(v) for v in kw_results.values())
        return {
            "mode": "fallback",
            "answer": (
                f"AI search unavailable. "
                f"Keyword search found {total} result(s) for '{query}'."
            ),
            "matched": {
                k: [r["id"] for r in v]
                for k, v in kw_results.items()
            },
            "error": str(e)
        }


def _parse_ids(line: str) -> list:
    try:
        part = line.split(":", 1)[1].strip()
        part = part.replace("[", "").replace("]", "").strip()
        if not part:
            return []
        return [
            int(x.strip())
            for x in part.split(",")
            if x.strip().isdigit()
        ]
    except Exception:
        return []