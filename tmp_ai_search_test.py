import pandas as pd
from ai_search.search import ai_search

PLACEHOLDER_PROJECTS = [
    {"id": 1, "title": "Sample Project", "department_id": 1, "status": "Behind Schedule", "start_date": "2024-01-01", "expected_end_date": "2024-12-31", "budget_allocated": 1000000, "budget_utilized": 800000, "funding_source": "FMARD", "keywords": "maize, sheller"}
]
DEPT_MAP = {1: "FPM"}
DEPT_FULL = {1: "Farm Power & Machinery"}

df = pd.DataFrame(PLACEHOLDER_PROJECTS)
result = ai_search('Which projects are currently behind schedule?', df, DEPT_MAP, DEPT_FULL)
print(result)
