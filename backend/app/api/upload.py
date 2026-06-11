from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.pdf_service import extract_text_from_pdf

from app.rag.chunker import split_text
from app.rag.embedding_service import create_embedding
from app.rag.chroma_service import add_document

router = APIRouter()

UPLOAD_FOLDER = "uploads"


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract PDF text
    extracted_text = extract_text_from_pdf(file_path)

    # Split text into chunks
    chunks = split_text(extracted_text)

    # Save chunks into ChromaDB
    for chunk in chunks:

        embedding = create_embedding(chunk)

        add_document(
            chunk=chunk,
            embedding=embedding,
            source=file.filename
        )

    return {
        "message": "PDF processed successfully",
        "chunks_saved": len(chunks)
    }