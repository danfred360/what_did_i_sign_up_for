from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

search_router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    filters: dict | None = None

class SearchResponse(BaseModel):
    count: int
    results: list[dict]

search_responses= {
    500: {"description": "Not implemented"},
}

# given input query, return list of document segments that are semantically similar to the query

@search_router.post("/search", response_model=SearchResponse, responses=search_responses, tags=['search'])
async def search(search_query: SearchQuery):
    raise HTTPException(status_code=500, detail="Not implemented")