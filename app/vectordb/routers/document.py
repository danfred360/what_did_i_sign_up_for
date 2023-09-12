from fastapi import APIRouter, HTTPException
from ..provider import VectorDBProvider

document_router = APIRouter()

@document_router.get("/documents", tags=['document'])
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

@document_router.post("/documents", tags=['document'])
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