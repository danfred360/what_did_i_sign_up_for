from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from ..provider import VectorDBProvider, RecordNotFound

collection_router = APIRouter()

class Collection(BaseModel):
    id: int
    parent_collection_id: int | None = None
    name: str
    description: str | None = None
    image_url: str | None = None

class CreateCollection(BaseModel):
    parent_collection_id: int | None = None
    name: str
    description: str
    image_url: str | None = None

class UpdateCollection(BaseModel):
    parent_collection_id: int | None = None
    name: str | None = None
    description: str | None = None
    image_url: str | None = None


@collection_router.get("/collections/{collection_id}", response_model=Collection, tags=['collection'])
async def get_collection(collection_id: int):
    provider = VectorDBProvider()
    provider.connect()
    collection = provider.get_collection_by_id(collection_id)
    provider.disconnect()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@collection_router.get("/collections", response_model=list[Collection], tags=['collection'])
async def list_collections():
    provider = VectorDBProvider()
    provider.connect()
    collections = provider.list_collections()
    provider.disconnect()
    if not collections:
        raise HTTPException(status_code=404, detail="Collections not found")
    return collections

@collection_router.patch("/collections/{collection_id}/update", response_model=Collection, tags=['collection'])
async def update_collection(collection_id: int, collection: UpdateCollection):
    provider = VectorDBProvider()
    provider.connect()
    collection = provider.update_collection(collection_id, collection.name, collection.description, collection.parent_collection_id, collection.image_url)
    provider.disconnect()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

delete_responses = {
    204: {"description": "Collection deleted"},
    404: {"description": "Collection not found"},
    500: {"description": "Something went wrong"}
}

@collection_router.delete("/collections/{collection_id}/delete", responses=delete_responses, tags=['collection'])
async def delete_collection(collection_id: int):
    provider = VectorDBProvider()
    provider.connect()
    try:
        response = provider.delete_collection(collection_id)
    except RecordNotFound:
        provider.disconnect()
        raise HTTPException(status_code=404, detail="Collection not found")
    provider.disconnect()
    if response == True:
        return Response(status_code=204)
    else:
        return HTTPException(status_code=500, detail="Something went wrong")

@collection_router.post("/collections/", response_model=Collection, tags=['collection'])
async def create_collection(collection: CreateCollection):
    provider = VectorDBProvider()
    provider.connect()
    collection = provider.create_collection(collection.name, collection.description, collection.parent_collection_id, collection.image_url)
    provider.disconnect()
    return collection
