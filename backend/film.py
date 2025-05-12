from fastapi import APIRouter, HTTPException, Header
from typing import List
from models import Film
from utils import decode_token

router = APIRouter()
films_db: List[Film] = []

@router.get("/", response_model=List[Film])
def get_all():
    return films_db

@router.get("/{film_id}", response_model=Film)
def get_film(film_id: int):
    for film in films_db:
        if film.id == film_id:
            return film
        raise HTTPException(status_code=404, detail="Film not found")
    
@router.post("/", response_model=Film)
def add_film(film: Film, authorization: str = Header(...)):
    user = decode_token(authorization.replace("Bearer ", ""))
    if user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add")
    for f in films_db:
        if f.id == film.id:
            raise HTTPException(status_code = 400 , detail ="Film already exists")
    films_db.append(film)
    return film