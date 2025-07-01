import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.embed import chunk_text
import google.generativeai as genai

# Gemini API key
genai.configure(api_key="AIzaSyAivjpLmnl_hYUq7rNSdHkEwYNRqrBIxoU")  # 🔁 Replace with your actual Gemini key

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

def load_faiss_index(index_path="vectors/index.faiss"):
    return faiss.read_index(index_path)

def load_chunks(txt_path="vectors/chunks.txt"):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.readlines()

def search_query(query, index, chunks, top_k=5):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), top_k)
    return [chunks[i] for i in indices[0]]

def answer_question(query, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer the question based on the context below:

Context:
{context}

Question: {query}
Answer:"""

    response = model.generate_content(prompt)
    return response.text.strip()
