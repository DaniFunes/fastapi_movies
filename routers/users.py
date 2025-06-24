from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from user_jwt import create_token, validate_token


loginUser = APIRouter()

class User(BaseModel):
    email: str
    password: str

@loginUser.post("/login", tags=["Authentication"])
def login(user: User):
    if user.email == 'danielito@gmail.com' and user.password == '123456':
        token: str = create_token(user.dict())
        return JSONResponse(content=token)
    return JSONResponse(content={'error': 'Usuario o contraseña incorrectos'}, status_code=401)