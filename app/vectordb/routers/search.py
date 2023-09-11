from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from psycopg2 import sql, Error as psycopg2Error
import logging
from ..provider import VectorDBProvider, RecordNotFound
from ..llm import LLMProvider

search_router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    document_id: int
    # filters: dict | None = None
    num_results: int | None = None

class SearchResponse(BaseModel):
    count: int
    results: list[dict]

search_responses= {
    500: {"description": "Server side error"},
}

# given input query, return list of document segments that are semantically similar to the query

def get_relevant_segments(query: str, filters: dict, num_segments: int = 5):
    if not query:
        raise ValueError('query is required')
    if filters and not isinstance(filters, dict):
        raise ValueError('filters must be an dict')
    if not isinstance(query, str):
        raise ValueError('Query must be a string')
    if not isinstance(num_segments, int):
        raise ValueError('Number of segments must be an integer')
    
    vectordb = VectorDBProvider()
    llm = LLMProvider()
    query_embedding = llm.get_embedding(query)

    table_name = "segment"
    embedding_column_name = "embedding"
    fields = ['id', 'document_id', 'content', 'created_at']

    select_query = "SELECT {fields} from {table}"
    if filters:
        query_parts = []
        if "document_ids" in filters:
            query_parts.append("document_id IN %s")
        if query_parts:
            select_query += " WHERE " + " AND ".join(query_parts)

    search_query = f"""
        SELECT {fields}
        FROM ({select_query}) AS relevant_segments
        ORDER BY {embedding_column_name} <-> CAST(%s AS vector)
        LIMIT %s
    """
    
    query = sql.SQL(search_query).format(
        fields=sql.SQL(',').join(map(sql.Identifier, fields)),
        select_query=sql.SQL(select_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name)
        ),
        embedding_column=sql.Identifier(embedding_column_name)
    )

    print(f"query: {query}")

    # sql.SQL('SELECT {fields} FROM {table} WHERE {column} = %s AND {embedding_column} <-> CAST(%s AS vector) LIMIT %s')

    try:
        vectordb.connect()
        if filters:
            if "document_ids" in filters:
                vectordb.cursor.execute(query, (tuple(filters["document_ids"]), query_embedding, num_segments,))
            else:
                vectordb.cursor.execute(query, (query_embedding, num_segments,))
    except Exception as e:
        vectordb.disconnect()
        raise e
    vectordb.disconnect()

    response =  vectordb.cursor.fetchall()
    if response:
        response_dict = [dict(zip(fields, row)) for row in response]
        return {'count': len(response_dict), 'results': response_dict}
    else:
        raise RecordNotFound("No segments found")
    
def get_relevant_segments_by_document_id(query: str, document_id: int, num_segments: int = 5):
    if not isinstance(document_id, int):
        raise ValueError('Document ID must be an integer')
    if not isinstance(query, str):
        raise ValueError('Query must be a string')
    if not isinstance(num_segments, int):
        raise ValueError('Number of segments must be an integer')

    vectordb = VectorDBProvider()
    llm = LLMProvider()
    query_embedding = llm.get_embedding(query)

    table_name = "segment"
    embedding_column_name = "embedding"
    fields = ['id', 'document_id', 'content', 'embedding', 'created_at']
    select_query = "SELECT {fields} from {table} WHERE document_id = %s"

    search_query = """
        SELECT {fields}
        FROM ({base_query}) AS relevant_segments
        ORDER BY {embedding_column_name} <-> CAST(%s AS vector)
        LIMIT %s
    """

    query = sql.SQL(search_query).format(
        fields=sql.SQL(',').join(map(sql.Identifier, fields)),
        base_query=sql.SQL(select_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name)
        ),
        embedding_column_name=sql.Identifier(embedding_column_name)
    )

    try:
        vectordb.connect()
        vectordb.cursor.execute(query, (document_id, query_embedding, num_segments,))
        query_result = vectordb.cursor.fetchall()
        results = [dict(zip(fields, row)) for row in query_result]
        for result in results:
            del result['embedding']
        return {'count': len(results), 'results': results}
    except psycopg2Error as e:
        logging.error(f"Error executing query: {e}")
        logging.info(f"Query: {query.as_string(vectordb.cursor)}")
        raise e
    except Exception as e:
        raise e
    finally:
        vectordb.disconnect()

def get_relevant_segments(query: str, num_requests: int = 5):
    if not isinstance(query, str):
        raise ValueError('Query must be a string')
    if not isinstance(num_requests, int):
        raise ValueError('Number of requests must be an integer')

    vectordb = VectorDBProvider()
    llm = LLMProvider()
    query_embedding = llm.get_embedding(query)

    table_name = "segment"
    embedding_column_name = "embedding"
    fields = ['id', 'document_id', 'content', 'embedding', 'created_at']
    select_query = "SELECT {fields} from {table}"

    search_query = """
        SELECT {fields}
        FROM ({base_query}) AS relevant_segments
        ORDER BY {embedding_column_name} <-> CAST(%s AS vector)
        LIMIT %s
    """

    query = sql.SQL(search_query).format(
        fields=sql.SQL(',').join(map(sql.Identifier, fields)),
        base_query=sql.SQL(select_query).format(
            fields=sql.SQL(',').join(map(sql.Identifier, fields)),
            table=sql.Identifier(table_name)
        ),
        embedding_column_name=sql.Identifier(embedding_column_name)
    )

    try:
        vectordb.connect()
        vectordb.cursor.execute(query, (query_embedding, num_requests,))
        query_result = vectordb.cursor.fetchall()
        results = [dict(zip(fields, row)) for row in query_result]
        for result in results:
            del result['embedding']
        return {'count': len(results), 'results': results}
    except psycopg2Error as e:
        logging.error(f"Error executing query: {e}")
        logging.info(f"Query: {query.as_string(vectordb.cursor)}")
        raise e
    except Exception as e:
        raise e
    finally:
        vectordb.disconnect()

@search_router.get("/search", response_model=SearchResponse, responses=search_responses, tags=['search'])
async def search(query: str, num_results: int = 5):
    provider = VectorDBProvider()
    try:
        provider.connect()
        results = get_relevant_segments(query, num_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        provider.disconnect()
    return results

@search_router.get("/documents/{document_id}/search", response_model=SearchResponse, responses=search_responses, tags=['search'])
async def search_document(document_id: int, query: str, num_results: int = 5):
    provider = VectorDBProvider()
    try:
        provider.connect()
        results = get_relevant_segments_by_document_id(query, document_id, num_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        provider.disconnect()
    return results

@search_router.get("/documents", tags=['search'])
async def list_documents():
    provider = VectorDBProvider()
    try:
        provider.connect()
        documents = provider.list_documents()
    except Exception as e:
        provider.disconnect()
        raise HTTPException(status_code=500, detail=str(e))
    provider.disconnect()
    return documents

@search_router.post("/documents", tags=['search'])
async def get_document_by_name(name: str):
    provider = VectorDBProvider()
    try:
        provider.connect()
        document = provider.get_file_document_by_name(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        provider.disconnect()
    return document