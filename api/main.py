from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import shutil

from app.embed import run_embedding_pipeline
from app.search import load_faiss_index, load_chunks, search_query, answer_question

app = FastAPI()

UPLOAD_DIR = "data/"
CHUNK_FILE = "vectors/chunks.txt"
INDEX_FILE = "vectors/index.faiss"

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure directory exists

        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunks = run_embedding_pipeline(file_location)

        return {
            "status": "success",
            "message": f"{file.filename} processed and indexed.",
            "chunks": len(chunks)
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "message": "Failed to upload or process the file."
        })


@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        index = load_faiss_index(INDEX_FILE)
        chunks = load_chunks(CHUNK_FILE)
        top_chunks = search_query(question, index, chunks)
        answer = answer_question(question, top_chunks)
        return {"question": question, "answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
