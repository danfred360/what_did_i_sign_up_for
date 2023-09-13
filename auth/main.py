from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.security import OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64decode
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel

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
users_db = {"username1": {"username": "username1", "hashed_password": pwd_context.hash("password1")}}
SECRET_KEY = "my_secret_key"

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

@app.post("/token", response_model=Token)
async def login_for_access_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or "Basic " not in auth_header:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    b64_encoded_creds = auth_header.split(" ")[1]
    decoded_creds = b64decode(b64_encoded_creds).decode("utf-8")
    username, _, password = decoded_creds.partition(":")

    user = users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
