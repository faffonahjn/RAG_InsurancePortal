import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
from app.ingest import ingest_document
from app.generator import generate_answer

app = FastAPI(
    title="RAG Insurance Portal",
    description="AI-powered document Q&A for insurance policies",
    version="1.0.0"
)

# ── REQUEST MODELS ────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str

# ── ENDPOINTS ─────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "running", "app": "RAG Insurance Portal"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF and ingest it into the vector store."""
    save_path = f"data/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    ingest_document(save_path)
    return {"message": f"{file.filename} ingested successfully"}


@app.post("/ask")
def ask_question(request: QueryRequest):
    """Ask a question against the ingested documents."""
    result = generate_answer(request.question)
    return result