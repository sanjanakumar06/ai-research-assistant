
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from app.routes.documents import router as documents_router
from app.routes.questions import router as questions_router

app = FastAPI(
    title="AI Research Assistant API",
    description="Locally hosted PDF-based RAG research assistant",
    version="0.2.0"
)

app.include_router(documents_router)
app.include_router(questions_router)


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
