import os
import sys
import pdfplumber
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# ── 1. LOAD ──────────────────────────────────────────────
def load_pdf(filepath: str) -> str:
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    print(f"Loaded {len(text)} characters from {filepath}")
    return text


# ── 2. CHUNK ─────────────────────────────────────────────
def chunk_text(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(text)
    print(f"Created {len(chunks)} chunks")
    return chunks


# ── 3. EMBED + STORE ─────────────────────────────────────
def embed_and_store(chunks: list, persist_dir: str = "vectorstore") -> Chroma:
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    print(f"Stored {len(chunks)} chunks in vector database at '{persist_dir}'")
    return vectorstore


# ── MASTER FUNCTION ───────────────────────────────────────
def ingest_document(filepath: str) -> Chroma:
    text = load_pdf(filepath)
    chunks = chunk_text(text)
    vectorstore = embed_and_store(chunks)
    return vectorstore


# ── RUN DIRECTLY TO TEST ──────────────────────────────────
if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "data/insurance_policy.pdf"
    ingest_document(filepath)
    print("Ingestion complete.")