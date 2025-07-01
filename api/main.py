from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import os
import traceback

from app.embed import run_embedding_pipeline
from app.search import load_faiss_index, load_chunks, search_query, answer_question

app = FastAPI()

UPLOAD_DIR = "data/"
CHUNK_FILE = "vectors/chunks.txt"
INDEX_FILE = "vectors/index.faiss"

# ✅ Custom handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request", "details": str(exc)}
    )

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        # ✅ Proper async file read (fixes ChunkedEncodingError on Render)
        contents = await file.read()
        with open(file_location, "wb") as f:
            f.write(contents)

        # ✅ Process embeddings
        chunks = run_embedding_pipeline(file_location)

        return {
            "status": "success",
            "message": f"{file.filename} processed and indexed.",
            "chunks": len(chunks)
        }

    except Exception as e:
        # ✅ Full error logging
        error_details = traceback.format_exc()
        print("Upload Error:\n", error_details)

        return JSONResponse(status_code=500, content={
            "error": str(e),
            "details": error_details
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
