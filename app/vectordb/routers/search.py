from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from psycopg2 import sql
from ..provider import VectorDBProvider, RecordNotFound
from ..llm import LLMProvider

search_router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    document_id: int
    num_results: int | None = None
    # filters: dict | None = None

class SearchResponse(BaseModel):
    count: int
    results: list[dict]

search_responses= {
    500: {"description": "Server side error"},
}

# given input query, return list of document segments that are semantically similar to the query

def get_relevant_segments(document_id, query, num_segments=5):
    if not document_id or not query:
        raise ValueError('Document id and query are required')
    if not isinstance(document_id, int):
        raise ValueError('Document id must be an integer')
    if not isinstance(query, str):
        raise ValueError('Query must be a string')
    if not isinstance(num_segments, int):
        raise ValueError('Number of segments must be an integer')
    
    vectordb = VectorDBProvider()
    llm = LLMProvider()
    query_embedding = llm.get_embedding(query)
    
    table_name = "segment"
    column_name = "document_id"
    embedding_column_name = "embedding"
    fields = ['id', 'document_id', 'content', 'created_at']
    query = sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s AND {embedding_column} <-> CAST(%s AS vector) LIMIT %s').format(
        fields=sql.SQL(',').join(map(sql.Identifier, fields)),
        table=sql.Identifier(table_name),
        column=sql.Identifier(column_name),
        embedding_column=sql.Identifier(embedding_column_name)
    )

    try:
        vectordb.connect()
        vectordb.cursor.execute(query, (document_id, query_embedding, num_segments,))
    except Exception as e:
        vectordb.disconnect()
        raise e

    response =  vectordb.cursor.fetchall()
    if response:
        response_dict = [dict(zip(fields, row)) for row in response]
        return {'count': len(response_dict), 'results': response_dict}
    else:
        raise RecordNotFound("No segments found")

@search_router.post("/search", response_model=SearchResponse, responses=search_responses, tags=['search'])
async def search(search_query: SearchQuery):
    provider = VectorDBProvider()
    try:
        provider.connect()
        if search_query.num_results == None:
            results = get_relevant_segments(search_query.document_id, search_query.query)
        else:
            results = get_relevant_segments(search_query.document_id, search_query.query, search_query.num_results)
    except Exception as e:
        provider.disconnect()
        raise HTTPException(status_code=500, detail=str(e))
    provider.disconnect()
    return {
        "count": len(results),
        "results": results
    }
    # raise HTTPException(status_code=500, detail="Not implemented")