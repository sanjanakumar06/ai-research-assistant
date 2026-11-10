
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from app.services.pdf_processor import extract_pdf_pages
from app.services.chunker import chunk_document
from app.services.vector_store import store_chunks, search_chunks

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_FILE_SIZE = 10 * 1024 * 1024


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

    document_id = str(uuid4())

    chunks = chunk_document(
        pages=pages,
        filename=file.filename or "uploaded.pdf"
    )

    if not chunks:
        raise HTTPException(
            status_code=422,
            detail="No extractable text found in PDF"
        )

    try:
        store_chunks(chunks, document_id)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to index document"
        )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "message": "Document uploaded and indexed successfully"
    }


@router.get("/search")
def search_documents(
    query: str = Query(min_length=1),
    top_k: int = Query(default=5, ge=1, le=20)
):
    results = search_chunks(query, top_k)

    matches = []

    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        matches.append({
            "text": text,
            "filename": metadata["filename"],
            "page_number": metadata["page_number"],
            "distance": distance
        })

    return {
        "query": query,
        "matches": matches
    }
