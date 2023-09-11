from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .vectordb.routers.collection import collection_router
from .vectordb.routers.file_class import file_class_router
from .vectordb.routers.file import file_router
from .vectordb.routers.search import search_router
from .vectordb.routers.question import question_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

root = os.path.dirname(os.path.abspath(__file__))

app.mount('/public', app=StaticFiles(directory='app/public', html=True), name='public')

@app.get("/")
async def redirect():
    response = RedirectResponse(url='/public')
    return response

app.include_router(collection_router)
app.include_router(file_class_router)
app.include_router(file_router)
app.include_router(search_router)
app.include_router(question_router)
