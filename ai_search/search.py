import os
import json
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def keyword_search(query: str, projects_df: pd.DataFrame, dept_map: dict) -> pd.DataFrame:
    """
    Fallback keyword search across title, summary, keywords, status, department.
    """
    if projects_df.empty:
        return pd.DataFrame()

    query_lower = query.lower()
    df = projects_df.copy()
    df["dept_name"] = df["department_id"].map(dept_map).fillna("").str.lower()

    mask = (
        df["title"].str.lower().str.contains(query_lower, na=False) |
        df.get("summary", pd.Series([""] * len(df))).str.lower().str.contains(query_lower, na=False) |
        df.get("keywords", pd.Series([""] * len(df))).str.lower().str.contains(query_lower, na=False) |
        df.get("status", pd.Series([""] * len(df))).str.lower().str.contains(query_lower, na=False) |
        df["dept_name"].str.contains(query_lower, na=False) |
        df.get("funding_source", pd.Series([""] * len(df))).str.lower().str.contains(query_lower, na=False)
    )

    return df[mask].drop(columns=["dept_name"], errors="ignore")


def build_context(projects_df: pd.DataFrame, dept_map: dict, dept_full: dict) -> str:
    """
    Converts the projects dataframe into a clean text context for the LLM.
    Limits to 60 projects to stay within token limits.
    """
    if projects_df.empty:
        return "No project data is currently available in the database."

    df = projects_df.copy()
    df["department"] = df["department_id"].map(dept_full).fillna("Unknown")
    df = df.head(60)

    lines = []
    for _, row in df.iterrows():
        line = (
            f"Project ID {row['id']}: \"{row['title']}\" | "
            f"Department: {row['department']} | "
            f"Status: {row.get('status', 'N/A')} | "
            f"Start: {row.get('start_date', 'N/A')} | "
            f"Expected End: {row.get('expected_end_date', 'N/A')} | "
            f"Budget Allocated: ₦{row.get('budget_allocated', 'N/A'):,} | "
            f"Budget Utilized: ₦{row.get('budget_utilized', 'N/A'):,} | "
            f"Funding: {row.get('funding_source', 'N/A')} | "
            f"Keywords: {row.get('keywords', 'N/A')}"
        )
        lines.append(line)

    return "\n".join(lines)


def ai_search(
    query: str,
    projects_df: pd.DataFrame,
    dept_map: dict,
    dept_full: dict
) -> dict:
    """
    Main search function.
    Returns:
        {
            "mode": "ai" | "keyword" | "fallback",
            "answer": str,
            "matched_ids": list[int],
            "error": str | None
        }
    """
    # ── GROQ AI SEARCH ────────────────────────────────────────────────────
    try:
        context = build_context(projects_df, dept_map, dept_full)

        system_prompt = """You are a research intelligence assistant for the National Centre for Agricultural Mechanization (NCAM) in Nigeria.

You are given a list of research projects from NCAM's database and a question from a user — either a department head, the Executive Director, or a staff member.

Your job is to:
1. Answer the question accurately using only the project data provided.
2. Return a clear, direct answer in plain English.
3. List the relevant Project IDs at the end of your response in this exact format:
   MATCHED_IDS: [1, 4, 7]

Rules:
- Only use information from the project data provided. Do not invent data.
- If no projects match the question, say so clearly and return MATCHED_IDS: []
- Keep answers concise — 3 to 6 sentences maximum.
- Always end with the MATCHED_IDS line, even if empty.
- Amounts are in Nigerian Naira (₦).
"""

        user_message = f"""Project Database:
{context}

Question: {query}"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            max_tokens=600
        )

        raw_answer = response.choices[0].message.content.strip()

        # ── Extract matched IDs ──
        matched_ids = []
        if "MATCHED_IDS:" in raw_answer:
            parts = raw_answer.split("MATCHED_IDS:")
            answer_text = parts[0].strip()
            id_part = parts[1].strip()
            try:
                id_part_clean = id_part.replace("[", "").replace("]", "").strip()
                if id_part_clean:
                    matched_ids = [
                        int(x.strip())
                        for x in id_part_clean.split(",")
                        if x.strip().isdigit()
                    ]
            except Exception:
                matched_ids = []
        else:
            answer_text = raw_answer

        return {
            "mode": "ai",
            "answer": answer_text,
            "matched_ids": matched_ids,
            "error": None
        }

    except Exception as e:
        # ── FALLBACK TO KEYWORD SEARCH ────────────────────────────────────
        keyword_results = keyword_search(query, projects_df, dept_map)
        matched_ids = keyword_results["id"].tolist() if not keyword_results.empty else []

        if matched_ids:
            answer = (
                f"AI search is temporarily unavailable. "
                f"Keyword search found {len(matched_ids)} project(s) matching '{query}'."
            )
        else:
            answer = (
                f"AI search is temporarily unavailable and no keyword matches "
                f"were found for '{query}'. Try different search terms."
            )

        return {
            "mode": "fallback",
            "answer": answer,
            "matched_ids": matched_ids,
            "error": str(e)
        }