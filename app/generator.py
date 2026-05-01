import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
from dotenv import load_dotenv
from groq import Groq
from app.retriever import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query: str) -> dict:
    # Step 1: Retrieve relevant chunks
    chunks = retrieve(query, k=3)
    context = "\n\n".join([doc.page_content for doc in chunks])

    # Step 2: Build prompt
    prompt = f"""You are an insurance policy assistant. Answer the question using ONLY the context provided below. 
If the answer is not in the context, say "I could not find that information in the policy document."

Context:
{context}

Question: {query}

Answer:"""

    # Step 3: Generate answer
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=500
    )

    answer = response.choices[0].message.content

    return {
        "query": query,
        "answer": answer,
        "sources": [doc.page_content[:100] + "..." for doc in chunks]
    }


if __name__ == "__main__":
    questions = [
        "What is the maximum limit for third party liability?",
        "What perils are covered under Section 1?",
        "What is the money limit if not stored in a safe?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        result = generate_answer(q)
        print(f"A: {result['answer']}")
        print("-" * 50)