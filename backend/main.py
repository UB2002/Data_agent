from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, ask

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://data-agent-pi.vercel.app"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(ask.router)

@app.get('/')
def index():
    return {"message":"hello"}

