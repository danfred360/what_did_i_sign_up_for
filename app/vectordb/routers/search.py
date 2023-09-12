from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..search import SearchProvider

search_router = APIRouter()

class SearchResponse(BaseModel):
    count: int
    results: list[dict]

search_responses= {
    500: {"description": "Server side error"},
}

@search_router.get("/search", response_model=SearchResponse, responses=search_responses, tags=['semantic search'])
async def global_search(query: str, num_results: int = 5):
    search = SearchProvider()
    try:
        results = search.get_relevant_segments(query, num_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return results

@search_router.get("/documents/{document_id}/search", response_model=SearchResponse, responses=search_responses, tags=['semantic search'])
async def search_by_document(document_id: int, query: str, num_results: int = 5):
    search = SearchProvider()
    try:
        results = search.get_relevant_segments_by_document_id(query, document_id, num_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return results

@search_router.get("/files/{file_id}/search", response_model=SearchResponse, responses=search_responses, tags=['semantic search'])
async def search_by_file(file_id: int, query: str, num_results: int = 5):
    search = SearchProvider()
    try:
        results = search.get_relevant_segments_by_file_id(query, file_id, num_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return results