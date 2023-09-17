from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64decode
from passlib.context import CryptContext
import jwt
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from .vectordb import VectorDBProvider

load_dotenv('.env')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
http_basic = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY")

provider = VectorDBProvider()

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateUser(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

@app.post("/create_user", response_model=Token)
async def create_user(user: CreateUser):
    plain_password = user.password
    salt = os.urandom(16)
    hashed_password = pwd_context.hash(plain_password + salt.hex())
    provider.connect()
    try:
        provider.create_user(user.username, hashed_password, salt.hex())
        access_token = create_access_token(data={"sub": user.username})
    finally:
        provider.disconnect()
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
async def login_for_access_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or "Basic " not in auth_header:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    b64_encoded_creds = auth_header.split(" ")[1]
    decoded_creds = b64decode(b64_encoded_creds).decode("utf-8")
    username, _, password = decoded_creds.partition(":")

    provider.connect()
    try:
        user = provider.get_user(username)
    finally:
        provider.disconnect()

    if not user or not verify_password(password + user["salt"], user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
