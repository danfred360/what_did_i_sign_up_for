from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..provider import VectorDBProvider
from datetime import datetime

document_router = APIRouter()

class Document(BaseModel):
    id: int
    file_id: int
    name: str
    description: str | None = None
    contents: str | None = None
    url: str
    created_at: datetime
    updated_at: datetime

class CreateDocument(BaseModel):
    name: str
    description: str | None = None
    contents: str | None = None
    url: str

class UpdateDocument(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    contents: str | None = None
    url: str | None = None

@document_router.get("/documents/{document_name}", tags=['document'])
async def get_document_by_name(document_name: str):
    provider = VectorDBProvider()
    try:
        provider.connect()
        document = provider.get_file_document_by_name(document_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        provider.disconnect()
    return document

@document_router.get("/documents/{document_id}", response_model=Document, tags=['document'])
async def get_file_document(document_id: int):
    provider = VectorDBProvider()
    provider.connect()
    document = provider.get_file_document(document_id)
    provider.disconnect()
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return document

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

@document_router.get("/files/{file_id}/documents", response_model=list[Document], tags=['document'])
async def list_file_documents(file_id: int):
    provider = VectorDBProvider()
    provider.connect()
    documents = provider.list_file_documents(file_id)
    provider.disconnect()
    if not documents:
        raise HTTPException(status_code=404, detail="documents not found")
    return documents

@document_router.post("/files/{file_id}/documents/create", response_model=Document, tags=['document'])
async def create_file_document(file_id: int, document: CreateDocument):
    provider = VectorDBProvider()
    provider.connect()
    document = provider.create_file_document(file_id, document.name, document.description, document.contents, document.url)
    provider.disconnect()
    return document

@document_router.patch("/files/{file_id}/documents/{document_id}/update", response_model=Document, tags=['document'])
async def update_file_document(file_id: int, document_id: int, document: UpdateDocument):
    provider = VectorDBProvider()
    provider.connect()
    document = provider.update_file_document(document_id, document.name, document.description, document.contents, document.url)
    provider.disconnect()
    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    return document

@document_router.delete("/files/{file_id}/documents/{document_id}/delete", tags=['document'])
async def delete_file_document(file_id: int, document_id: int):
    provider = VectorDBProvider()
    provider.connect()
    try:
        response = provider.delete_file_document(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    provider.disconnect()
    if response is True:
        return '', 204
    else:
        return HTTPException(status_code=500, detail="Something went wrong")
