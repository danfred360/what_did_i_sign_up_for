from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..question import QuestionAnswerer

question_router = APIRouter()

class QuestionResponse(BaseModel):
    answer: str

question_responses= {
    500: {"description": "Not implemented"}
}

@question_router.get("/question", response_model=QuestionResponse, responses=question_responses, tags=['question'])
async def question(question: str):
    answerer = QuestionAnswerer()
    try:
        answer = answerer.answer_question(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {e}")
    return answer