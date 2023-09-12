from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from ..provider import VectorDBProvider, RecordNotFound
from datetime import datetime

file_router = APIRouter()

class File(BaseModel):
    id: int
    collection_id: int
    file_class_id: int
    name: str
    description: str | None = None
    url: str
    created_at: datetime
    updated_at: datetime

class CreateFile(BaseModel):
    collection_id: int
    file_class_id: int
    name: str
    description: str | None = None
    url: str

class UpdateFile(BaseModel):
    collection_id: int | None = None
    file_class_id: int | None = None
    name: str | None = None
    description: str | None = None
    url: str | None = None

@file_router.get("/files/{file_id}", response_model=File, tags=['file'])
async def get_file(file_id: int):
    provider = VectorDBProvider()
    provider.connect()
    file = provider.get_file(file_id)
    provider.disconnect()
    if not file:
        raise HTTPException(status_code=404, detail="file not found")
    return file

@file_router.get("/files", response_model=list[File], tags=['file'])
async def list_files():
    provider = VectorDBProvider()
    provider.connect()
    files = provider.list_files()
    provider.disconnect()
    if not files:
        raise HTTPException(status_code=404, detail="files not found")
    return files

@file_router.patch("/files/{file_id}/update", response_model=File, tags=['file'])
async def update_file(file_id: int, file: UpdateFile):
    provider = VectorDBProvider()
    provider.connect()
    file = provider.update_file(file_id, file.collection_id, file.file_class_id, file.name, file.description, file.url)
    provider.disconnect()
    if not file:
        raise HTTPException(status_code=404, detail="file not found")
    return file

delete_responses = {
    204: {"description": "File class deleted"},
    404: {"description": "File class not found"},
    500: {"description": "Something went wrong"}
}

@file_router.delete("/files/{file_id}/delete", response_model=File, responses=delete_responses, tags=['file'])
async def delete_file(file_id: int):
    provider = VectorDBProvider()
    try:
        provider.connect()
        response = provider.delete_file(file_id)
    except RecordNotFound:
        provider.disconnect()
        raise HTTPException(status_code=404, detail="file not found")
    provider.disconnect()
    if response is True:
        return Response(status_code=204)

@file_router.post("/files", response_model=File, tags=['file'])
async def create_file(file: CreateFile):
    provider = VectorDBProvider()
    provider.connect()
    file = provider.create_file(file.collection_id, file.file_class_id, file.name, file.description, file.url)
    provider.disconnect()
    if not file:
        raise HTTPException(status_code=404, detail="file not found")
    return file
