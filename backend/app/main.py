
from fastapi import FastAPI
from app.routes.documents import router as documents_router

app = FastAPI(
    title="AI Research Assistant API",
    description="Backend for a PDF-based RAG research assistant",
    version="0.1.0"
)

app.include_router(documents_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Research Assistant API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
