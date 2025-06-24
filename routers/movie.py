from fastapi import  Path, Query , Depends, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from user_jwt import create_token, validate_token



routerMovie = APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'danielito@gmail.com':
            raise HTTPException(status_code=403, detail="Credenciales incorrectas")


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default= 'Título de la película',min_length=2, max_length=60)
    director: str = Field(default= 'Director de la película',min_length=3, max_length=60)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director
        }

@routerMovie.get("/movies", tags=["Movies"], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))


@routerMovie.get("/movies/{id}", tags=["Movies por id"], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Película no encontrada'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerMovie.get("/movies/", tags=["Movies por categorias"])
def get_movies_by_director(director: str = Query(min_length=3, max_length=50)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.director == director).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerMovie.post('/movies', tags=["Movies"], status_code=201)
def create_movie(movie : Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={'message': 'Se ha creado una nueva película', 'movie': movie.to_dict()})


@routerMovie.put('/movies/{id}', tags=["Movies"])
def update_movie(id : int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={'message': 'Película no encontrada'}, status_code=404)
    data.title = movie.title
    data.director = movie.director
    db.commit()
    return JSONResponse(content={'message': 'Se ha actualizado la película'})

@routerMovie.delete('/movies/{id}', tags=["Movies"])
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={'message': 'Película no encontrada'}, status_code=404)
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message": "Movie not found"})