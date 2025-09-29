# RAG Excel App

## Project Overview

RAG Excel App is a FastAPI-based backend and React frontend services that enables users to upload Excel files, ask natural language questions about the data, and receive answers powered by LLMs (like Gemini). The app automatically creates database tables from uploaded Excel sheets, generates SQL queries from user questions, and returns results along with visual charts.

### Key Features
- **Excel Upload:** Upload `.xls` or `.xlsx` files; each sheet becomes a database table.
- **Session Management:** Each upload creates a unique session for data isolation.
- **Natural Language Q&A:** Ask questions about your data; the app uses an LLM to generate SQL and answers.
- **SQL Generation:** Automatically generates and executes SQL queries based on your question.
- **Chart Visualization:** Returns results and a chart (as base64 PNG) for easy visualization.

## Backend Setup Instructions

1. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   *(Or manually install FastAPI, SQLAlchemy, pandas, matplotlib, uvicorn, etc.)*

2. **Run the FastAPI server:**
   ```sh
   uvicorn main:app --reload --port 3000
   ```

3. **Prepare your database:**
   - The app uses SQLite by default. The database file is `app.db`.
   - Tables are created automatically when you upload an Excel file.

## Frontend Setup Instructions



1. **Install dependencies:**
   ```sh
   npm install
   # or
   yarn install
   ```


2. **Run the frontend app:**
   ```sh
   npm run dev
   # or
   yarn dev
   ```


## API Usage

### 1. Upload Excel File
- **Endpoint:** `POST /upload`
- **Body:** `form-data` with key `file` (type: File)
- **Response:**
  ```json
  {
    "session_id": "...",
    "tables_created": ["table_xxx", ...]
  }
  ```

### 2. Ask a Question
- **Endpoint:** `POST /ask`
- **Body:** `raw` JSON
  ```json
  {
    "session_id": "<session_id_from_upload>",
    "question": "your question here"
  }
  ```
- **Response:**
  ```json
  {
    "answer": "...",
    "sql_query": "...",
    "results": [...],
    "chart": "<base64 PNG>"
  }
  ```


