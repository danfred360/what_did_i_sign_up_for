from fastapi import APIRouter, HTTPException
from ..loader import DocumentLoader

loader_router = APIRouter()

@loader_router.get("/loader", tags=['loader'])
async def load_documents_from_input_files_dir():
    loader = DocumentLoader()
    generate_embeddings = True
    try:
        result = loader.load_documents_from_input_files_dir(generate_embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result