from fastapi import APIRouter, HTTPException
from ..loader import DocumentLoader

loader_router = APIRouter()

@loader_router.get("/loader/load_input_files", tags=['loader'])
async def load_files_from_input_files_dir():
    loader = DocumentLoader()
    generate_embeddings = True
    try:
        result = loader.load_documents_from_input_files_dir(generate_embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result

@loader_router.get("/loader/load_url", tags=['loader'])
async def load_file_from_url(url: str):
    loader = DocumentLoader()
    generate_embeddings = True
    try:
        result = loader.load_file_from_url(url, generate_embeddings=generate_embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result

@loader_router.get("/files/{file_id}/process", tags=['loader'])
async def process_file(file_id: int):
    loader = DocumentLoader()
    generate_embeddings = True
    try:
        result = loader.process_file(file_id, generate_embeddings=generate_embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result