from http.client import HTTPException

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from user_jwt import validate_token
from fastapi.security import HTTPBearer
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.users import loginUser

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
