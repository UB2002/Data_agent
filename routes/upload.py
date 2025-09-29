from fastapi import APIRouter, UploadFile, HTTPException
import pandas as pd
from sqlalchemy import text
import uuid
from db import engine
from utils import clean_dataframe, generate_table_name, generate_session_id

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Only Excel files allowed")
    
    session_id = generate_session_id()
    xls = pd.ExcelFile(file.file)
    tables_created = []

    with engine.begin() as conn:
        # Insert session
        conn.execute(text("INSERT INTO sessions (id) VALUES (:id)"), {"id": session_id})

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df = clean_dataframe(df)
            table_name = generate_table_name()
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            # Save table info
            conn.execute(
                text("INSERT INTO tables (id, session_id, table_name, original_sheet_name) VALUES (:id, :sid, :tname, :sname)"),
                {"id": str(uuid.uuid4()), "sid": session_id, "tname": table_name, "sname": sheet_name}
            )
            tables_created.append(table_name)

    return {"session_id": session_id, "tables_created": tables_created}
