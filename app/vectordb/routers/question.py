from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..llm import LLMProvider

question_router = APIRouter()

class QuestionResponse(BaseModel):
    answer: str

question_responses= {
    500: {"description": "Not implemented"}
}

# given input query, return answer to question (if possible using source documents) and citations

@question_router.get("/question", response_model=QuestionResponse, responses=question_responses, tags=['question'])
async def question(question: str):
    llm = LLMProvider()
    try:
        answer = llm.answer_question(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {e}")
    return answer