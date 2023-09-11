from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

question_router = APIRouter()

class Question(BaseModel):
    query: str
    filters: dict | None = None

class QuestionResponse(BaseModel):
    count: int
    results: list[dict]

question_responses= {
    500: {"description": "Not implemented"}
}

# given input query, return answer to question (if possible using source documents) and citations

@question_router.post("/question", response_model=QuestionResponse, responses=question_responses, tags=['question'])
async def question(question_query: Question):
    raise HTTPException(status_code=500, detail="Not implemented")