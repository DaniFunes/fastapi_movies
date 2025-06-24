from http.client import HTTPException

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from user_jwt import validate_token
from fastapi.security import HTTPBearer
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.users import loginUser
import os

app = FastAPI(
    title="My FastAPI Application",
    description="Una API en los primeros pasos",
    version="0.0.1"
)

app.include_router(routerMovie)
app.include_router(loginUser)

Base.metadata.create_all(bind=engine)

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'danielito@gmail.com':
            raise HTTPException(status_code=403, detail="Credenciales incorrectas")


@app.get("/", tags=["Inicio"])
def read_root():
    return HTMLResponse('<H1>¡Hola, mundo!</H1>')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port = port)