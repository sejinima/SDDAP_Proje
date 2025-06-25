from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import sqlite3
import os
import requests
from .utils import hash_password

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

    class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

@router.post("/admin/users")
def create_user(user: UserCreate):
    conn = sqlite3.connect("db/movies.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            (user.username, user.email, hash_password(user.password), user.role)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Hata: {e}")
    finally:
        conn.close()

    return {"msg": "Kullanıcı başarıyla eklendi"}

class RoleUpdate(BaseModel):
    role: str  # "admin" veya "user"

@router.put("/admin/users/{user_id}/role")
def update_user_role(user_id: int, role_update: RoleUpdate):
    if role_update.role not in ("admin", "user"):
        raise HTTPException(status_code=400, detail="Geçersiz rol")

    conn = sqlite3.connect("db/movies.db")
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET role = ? WHERE id = ?", (role_update.role, user_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        conn.commit()
    finally:
        conn.close()

    return {"msg": "Rol başarıyla güncellendi"}
