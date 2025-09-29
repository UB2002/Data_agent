# RAG Excel App

## Setup Instructions

1. **Install Python dependencies:**
   ```sh
   py -m venv venv
   venv/Scripts/Activate
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server:**
   ```sh
   uvicorn main:app --reload --port 3000
   ```
   *(Change `main:app` if your FastAPI app is in a different file or variable)*

3. **Prepare your database:**
   - The app uses SQLite by default. The database file is `app.db`.
   - Tables are created automatically when you upload an Excel file.

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

### 3. View Chart
- The `chart` field is a base64-encoded PNG image. To view it:
  - copy the string and past it in the visualize.py file and run it for image
