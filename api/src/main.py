from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from .vectordb.routers.collection import collection_router
from .vectordb.routers.file_class import file_class_router
from .vectordb.routers.file import file_router
from .vectordb.routers.document import document_router
from .vectordb.routers.search import search_router
from .vectordb.routers.question import question_router
from .vectordb.routers.loader import loader_router
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="What did I sign up for?",
    description="Ingest terms of use and privacy policies, semantic search, and question answering."
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:19006",
    "http://192.168.200.236:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

oauth2_scheme = HTTPBearer()
SECRET_KEY = os.environ.get("SECRET_KEY")

class User(BaseModel):
    username: str

async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    authorization.split(" ")[1] if " " in authorization else authorization
    try:
        token_str = authorization.credentials
        payload = jwt.decode(token_str, SECRET_KEY, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
        return User(username=username)
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/users/me", response_model = User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    print(f'current_user: {current_user}')
    return current_user

app.include_router(search_router)
app.include_router(question_router)
app.include_router(loader_router)
app.include_router(document_router)
app.include_router(file_router)
app.include_router(collection_router)
app.include_router(file_class_router)

# root = os.path.dirname(os.path.abspath(__file__))
# app.mount('/staticapp', app=StaticFiles(directory='api/public', html=True), name='public')
@app.get("/", tags=['root'])
async def redirect_to_swagger():
    response = RedirectResponse(url='/docs')
    return response