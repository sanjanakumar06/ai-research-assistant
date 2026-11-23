
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.rag import answer_question


router = APIRouter(tags=["Questions"])


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)


@router.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        return answer_question(
            question=request.question.strip(),
            top_k=request.top_k
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer"
        )
