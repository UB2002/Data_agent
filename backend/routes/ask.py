from fastapi import APIRouter, HTTPException
import pandas as pd
from sqlalchemy import text
from models import AskRequest
from db import engine
from utils import generate_schema_prompt, run_gemini_query, generate_chart

router = APIRouter()

@router.post("/ask")
async def ask_question(req: AskRequest):
    with engine.connect() as conn:
        session_tables = conn.execute(
            text("SELECT table_name FROM tables WHERE session_id = :sid"),
            {"sid": req.session_id}
        ).fetchall()

    if not session_tables:
        raise HTTPException(404, "Invalid session or no tables found")

    # Currently, ask only on the first table; can extend to multi-table
    table_name = session_tables[0][0]

    df_sample = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", engine)
    schema = generate_schema_prompt(table_name, df_sample)
    sample_rows = df_sample.to_dict(orient="records")

    gemini_resp = run_gemini_query(req.question, schema, sample_rows)

    # Extract SQL block from Gemini response
    import re
    sql_query = None
    # Try to find SQL code block
    code_block = re.search(r"```sql(.*?)```", gemini_resp, re.DOTALL | re.IGNORECASE)
    if code_block:
        sql_query = code_block.group(1).strip()
    else:
        # Fallback: collect lines starting with SELECT until semicolon
        lines = gemini_resp.splitlines()
        collecting = False
        sql_lines = []
        for line in lines:
            if line.strip().lower().startswith("select"):
                collecting = True
            if collecting:
                sql_lines.append(line.strip())
                if ";" in line:
                    break
        if sql_lines:
            sql_query = " ".join(sql_lines).replace("```", "").strip()

    results = []
    print("###"*10)
    print(results)
    print("###"*10)
    if sql_query:
        try:
            with engine.connect() as conn:
                rows = conn.execute(text(sql_query)).fetchall()
                results = [dict(r._mapping) for r in rows]
        except Exception as e:
            results = [{"error": str(e)}]

    df_results = pd.DataFrame(results) if results else pd.DataFrame()
    chart = generate_chart(df_results) if not df_results.empty else None

    return {
        "answer": gemini_resp,
        "sql_query": sql_query,
        "results": results,
        "chart": chart
    }
