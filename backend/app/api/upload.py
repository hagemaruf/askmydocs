from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.pdf_service import extract_pages_from_pdf
from app.rag.chunker import split_text
from app.rag.embedding_service import create_embeddings
from app.rag.chroma_service import add_documents

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract pages
    pages = extract_pages_from_pdf(
        file_path
    )

    all_chunks = []

    all_embeddings = []

    all_metadatas = []

    # Process each page
    for page_data in pages:

        page_number = page_data["page"]

        text = page_data["text"]

        chunks = split_text(text)

        embeddings = create_embeddings(chunks)

        for i, chunk in enumerate(chunks):

            all_chunks.append(chunk)

            all_embeddings.append(
                embeddings[i]
            )

            all_metadatas.append({
                "source": file.filename,
                "page": page_number,
                "chunk": i
            })

    # Store in ChromaDB
    add_documents(
        all_chunks,
        all_embeddings,
        all_metadatas
    )

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "chunks": len(all_chunks)
    }