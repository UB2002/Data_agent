import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from google import genai
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Helpers ---
def clean_column(col: str, index: int = None) -> str:
    if not col or col.startswith("Unnamed"):
        return f"col_{index}"
    return col.strip().replace(" ", "_").replace("-", "_")

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Rename columns
    df.columns = [clean_column(c, i) for i, c in enumerate(df.columns)]
    
    # Clean each column by type
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip().fillna("Unknown")
        elif "int" in str(df[col].dtype) or "float" in str(df[col].dtype):
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        elif "datetime" in str(df[col].dtype):
            df[col] = pd.to_datetime(df[col], errors="coerce")
    df = df.drop_duplicates()
    return df

def generate_schema_prompt(table_name: str, df: pd.DataFrame) -> dict:
    cols = []
    for col, dtype in df.dtypes.items():
        if "int" in str(dtype):
            ctype = "int"
        elif "float" in str(dtype):
            ctype = "float"
        elif "datetime" in str(dtype):
            ctype = "datetime"
        else:
            ctype = "string"
        cols.append({"name": col, "type": ctype})
    return {"table": table_name, "columns": cols}


def run_gemini_query(question: str, schema: dict, sample_rows: list = None) -> str:
    prompt = f"""
                    You are an expert SQL analyst.
                    You are given the following table schema:
                    {schema}

                    Sample rows: {sample_rows if sample_rows else 'None'}

                    1. If needed, generate an SQL query.
                    2. Use only valid column names from the schema.
                    3. Return SQL query and a natural language answer.
                    4. If the question is vague, make reasonable assumptions.
            """
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"{prompt}\nUser question: {question}")

    return response.text


def generate_chart(df: pd.DataFrame, chart_type: str = "line") -> str:
    if df.empty:
        return None
    plt.figure(figsize=(10,6))
    try:
        if len(df.columns) == 1:
            # Single column: plot histogram/bar for numeric
            col = df.columns[0]
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].value_counts().plot(kind="bar")
                plt.xlabel(col)
                plt.ylabel("Count")
                plt.title(f"Distribution of {col}")
            else:
                df[col].value_counts().plot(kind="bar")
                plt.xlabel(col)
                plt.ylabel("Count")
                plt.title(f"Distribution of {col}")
        elif len(df.columns) >= 2:
            if chart_type == "line":
                df.plot(kind="line", x=df.columns[0], y=df.columns[1])
            elif chart_type == "bar":
                df.plot(kind="bar", x=df.columns[0], y=df.columns[1])
            elif chart_type == "pie":
                df.plot(kind="pie", y=df.columns[0], labels=df[df.columns[0]])
            else:
                return None
        else:
            return None
    except Exception as e:
        return None
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def generate_table_name() -> str:
    return f"table_{uuid.uuid4().hex[:8]}"


def generate_session_id() -> str:
    return str(uuid.uuid4())
