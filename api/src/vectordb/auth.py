from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import BaseModel
import os

class User(BaseModel):
    username: str

oauth2_scheme = HTTPBearer()

async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    try:
        token_str = authorization.credentials
        payload = jwt.decode(token_str, SECRET_KEY, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
        return User(username=username)
    except Exception as e:
        raise e
