from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.pdf_service import extract_text_from_pdf

router = APIRouter()

UPLOAD_FOLDER = "uploads"


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Validasi file PDF
    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    # Buat folder uploads jika belum ada
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Path file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Simpan file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    extracted_text = extract_text_from_pdf(file_path)

    return {
        "filename": file.filename,
        "text_preview": extracted_text[:1000]
    }