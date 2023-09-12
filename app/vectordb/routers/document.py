from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..provider import VectorDBProvider
document_router = APIRouter()
from datetime import datetime

class Document(BaseModel):
    id: int
    file_id: int
    name: str
    description: str | None = None
    contents: str | None = None
    url: str
    created_at: datetime
    updated_at: datetime

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