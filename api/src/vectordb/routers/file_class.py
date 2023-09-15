from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..provider import VectorDBProvider, RecordNotFound
from ..auth import get_current_user, User

file_class_router = APIRouter()

class FileClass(BaseModel):
    id: int
    name: str
    description: str | None = None
    image_url: str | None = None

class CreateFileClass(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None

class UpdateFileClass(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None

@file_class_router.get("/file_classes/{file_class_id}", response_model=FileClass, tags=['file_class'])
async def get_file_class(file_class_id: int, current_user: User = Depends(get_current_user)):
    provider = VectorDBProvider()
    provider.connect()
    file_class = provider.get_file_class(file_class_id)
    provider.disconnect()
    if not file_class:
        raise HTTPException(status_code=404, detail="file class not found")
    return file_class

@file_class_router.get("/file_classes", response_model=list[FileClass], tags=['file_class'])
async def list_file_classes(current_user: User = Depends(get_current_user)):
    provider = VectorDBProvider()
    provider.connect()
    file_classes = provider.list_file_classes()
    provider.disconnect()
    if not file_classes:
        raise HTTPException(status_code=404, detail="file classes not found")
    return file_classes

@file_class_router.post("/file_classes/", response_model=FileClass, tags=['file_class'])
async def create_file_class(file_class: CreateFileClass, current_user: User = Depends(get_current_user)):
    provider = VectorDBProvider()
    provider.connect()
    file_class = provider.create_file_class(file_class.name, file_class.description, file_class.image_url)
    provider.disconnect()
    if not file_class:
        raise HTTPException(status_code=500, detail="Something went wrong")
    else:
        return file_class

@file_class_router.patch("/file_classes/{file_class_id}/update", response_model=FileClass, tags=['file_class'])
async def update_file_class(file_class_id: int, file_class: UpdateFileClass, current_user: User = Depends(get_current_user)):
    provider = VectorDBProvider()
    provider.connect()
    file_class = provider.update_file_class(file_class_id, file_class.name, file_class.description, file_class.image_url)
    provider.disconnect()
    if not file_class:
        raise HTTPException(status_code=404, detail="file class not found")
    return file_class

delete_responses = {
    204: {"description": "File class deleted"},
    404: {"description": "File class not found"},
    500: {"description": "Something went wrong"}
}

@file_class_router.delete("file_class/{file_class_id}/delete", response_model=FileClass, responses=delete_responses, tags=['file_class'])
async def delete_file_class(file_class_id: int, current_user: User = Depends(get_current_user)):
    provider = VectorDBProvider()
    try:
        provider.connect()
        response = provider.delete_file_class(file_class_id)
    except RecordNotFound:
        provider.disconnect()
        raise HTTPException(status_code=404, detail="file class not found")
    provider.disconnect()
    if response is True:
        return '', 204
    else:
        return HTTPException(status_code=500, detail="Something went wrong")