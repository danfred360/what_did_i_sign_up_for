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

@question_router.get("/documents/{document_id}/question", response_model=QuestionResponse, responses=question_responses, tags=['question'])
async def question_by_document_id(document_id: int, question: str):
    answerer = QuestionAnswerer()
    try:
        answer = answerer.answer_question_by_document_id(question, document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {e}")
    return answer

@question_router.get("/files/{file_id}/question", response_model=QuestionResponse, responses=question_responses, tags=['question'])
async def question_by_file_id(file_id: int, question: str):
    answerer = QuestionAnswerer()
    try:
        answer = answerer.answer_question_by_file_id(question, file_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {e}")
    return answer

@question_router.get("/collections/{collection_id}/question", response_model=QuestionResponse, responses=question_responses, tags=['question'])
async def question_by_collection_id(collection_id: int, question: str):
    answerer = QuestionAnswerer()
    try:
        answer = answerer.answer_question_by_collection_id(question, collection_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {e}")
    return answer

@question_router.get("/file_classes/{file_class_id}/question", response_model=QuestionResponse, responses=question_responses, tags=['question'])
async def question_by_file_class_id(file_class_id: int, question: str):
    answerer = QuestionAnswerer()
    try:
        answer = answerer.answer_question_by_file_class_id(question, file_class_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {e}")
    return answer