from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from app.extract import extract_text

def chunk_text(text, max_chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i+max_chunk_size]) for i in range(0, len(words), max_chunk_size)]

def embed_chunks(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(chunks, show_progress_bar=True)

def save_faiss_index(embeddings, output_path="vectors/index.faiss"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure folder exists
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, output_path)

def save_chunks(chunks, path="vectors/chunks.txt"):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # Ensure folder exists
    with open(path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n")

def run_embedding_pipeline(file_path):
    text = extract_text(file_path)
    chunks = chunk_text(text)

    #  Prevent crashing if no text or empty chunks
    if not chunks or all(chunk.strip() == "" for chunk in chunks):
        raise ValueError("No valid content extracted from the document.")

    embeddings = embed_chunks(chunks)
    save_faiss_index(np.array(embeddings))
    save_chunks(chunks)
    return chunks
