# RAG Insurance Portal

AI-powered document Q&A for insurance policies. Upload any insurance PDF and ask questions in plain English — the system retrieves relevant policy sections and generates grounded, cited answers.

Built by a registered nurse turned ML engineer, with insurance domain expertise baked into the design.

---

## Architecture

```
PDF Upload → Text Extraction → Chunking → Embedding → Chroma Vector DB
                                                              ↓
User Question → Embed Query → Semantic Search → Top-K Chunks → Groq LLM → Answer
```

**Stack:**
- Embeddings: `all-MiniLM-L6-v2` (HuggingFace, runs locally)
- Vector DB: Chroma (persistent local store)
- LLM: Llama 3.1 via Groq API (free tier)
- API: FastAPI
- UI: Streamlit
- CI: GitHub Actions
- Container: Docker

---

## Live Demo

Upload the SIC Insurance Homeplus Policy PDF and ask:
- *"What perils are covered under Section 1?"*
- *"What is the money limit if not stored in a safe?"*
- *"How many months is rent covered after a loss?"*

---

## Quickstart

**1. Clone and setup:**

```bash
git clone https://github.com/faffonahjn/RAG_InsurancePortal.git
cd RAG_InsurancePortal
pip install -r requirements.txt
```

**2. Add your Groq API key (free at console.groq.com):**

```bash
echo "GROQ_API_KEY=your-key-here" > .env
```

**3. Ingest a document:**

```bash
python app/ingest.py data/insurance_policy.pdf
```

**4. Run the UI:**

```bash
streamlit run app/streamlit_app.py
```

**5. Or run the API:**

```bash
uvicorn app.api:app --reload
```

---

## Docker

```bash
docker build -t rag-insurance-portal .
docker-compose up
```

- API: `http://localhost:8000/docs`
- UI: `http://localhost:8501`

---

## Evaluation

```bash
python tests/test_pipeline.py
```

Current accuracy: **80% (4/5 test cases passing)**

---

## Project Structure

```
RAG_InsurancePortal/
├── app/
│   ├── ingest.py          # Stage 1: Load → Chunk → Embed → Store
│   ├── retriever.py       # Stage 2: Semantic search
│   ├── generator.py       # Stage 3: LLM generation
│   ├── api.py             # FastAPI endpoints
│   └── streamlit_app.py   # Chat UI
├── tests/
│   └── test_pipeline.py   # Retrieval accuracy evaluation
├── data/                  # PDF documents
├── vectorstore/           # Chroma persistent store
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Author

**Francis Affonah** — Registered Nurse → Clinical ML Engineer

[GitHub](https://github.com/faffonahjn) | [LinkedIn](https://linkedin.com/in/francis-affonah-23745a205)