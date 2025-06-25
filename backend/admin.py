from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import sqlite3
import os
import requests

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db/movies.db")  

class MovieInput(BaseModel):
    title: str
    year: int
    rating: float

@router.post("/admin/movies")
def add_movie(movie: MovieInput):
    # OMDb API'den poster çek
    api_key = "729dc000"
    omdb_url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie.title}&y={movie.year}"
    
    try:
        poster_url = ""
        response = requests.get(omdb_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("Poster") and data["Poster"] != "N/A":
                poster_url = data["Poster"]
    except Exception as e:
        print("Poster fetch hatası:", e)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO films (title, year, rating, poster_url)
            VALUES (?, ?, ?, ?)""",
            (movie.title, movie.year, movie.rating, poster_url))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Veritabanı hatası: {e}")
    finally:
        conn.close()

    return {"msg": "Film başarıyla eklendi"}
