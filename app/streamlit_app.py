import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import shutil
from app.ingest import ingest_document
from app.generator import generate_answer

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="RAG Insurance Portal",
    page_icon="🏥",
    layout="wide"
)

# ── HEADER ────────────────────────────────────────────────
st.title("🏥 RAG Insurance Portal")
st.caption("AI-powered document Q&A for insurance policies — powered by Groq + HuggingFace")

# ── SIDEBAR: FILE UPLOAD ──────────────────────────────────
with st.sidebar:
    st.header("📄 Upload Policy Document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file:
        save_path = f"data/{uploaded_file.name}"
        with open(save_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

        with st.spinner("Ingesting document..."):
            ingest_document(save_path)
        st.success(f"✅ {uploaded_file.name} ingested successfully")

    st.divider()
    st.markdown("**Built by Francis Affonah**")
    st.markdown("[GitHub](https://github.com/faffonahjn) | [LinkedIn](https://linkedin.com/in/francis-affonah-23745a205)")

# ── CHAT INTERFACE ────────────────────────────────────────
st.subheader("💬 Ask a Question")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Source Chunks"):
                for i, source in enumerate(message["sources"]):
                    st.caption(f"Chunk {i+1}: {source}")

# Chat input
if prompt := st.chat_input("Ask about your insurance policy..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching policy document..."):
            result = generate_answer(prompt)
            answer = result["answer"]
            sources = result["sources"]

        st.markdown(answer)
        with st.expander("📚 Source Chunks"):
            for i, source in enumerate(sources):
                st.caption(f"Chunk {i+1}: {source}")

    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })