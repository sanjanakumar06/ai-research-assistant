
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_processor import extract_pdf_pages

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 10 MB size limit"
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid PDF"
        )

    try:
        pages = extract_pdf_pages(content)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process PDF"
        )

    return {
        "filename": file.filename,
        "total_pages": len(pages),
        "pages": pages
    }
