from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import sqlite3
import os
import requests
from backend.utils import get_db_connection, hash_password
from backend.config import DB_PATH

router = APIRouter()


# === Film Ekleme ===
class MovieInput(BaseModel):
    title: str
    year: int  # int! (YIL)
    rating: float
    poster_url: str = ""

@router.post("/admin/movies")
def add_movie(movie: MovieInput):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO films (title, year, rating, poster_url)
            VALUES (?, ?, ?, ?)
        """, (movie.title, movie.year, movie.rating, movie.poster_url))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Veritabanı hatası: {e}")
    finally:
        conn.close()
    return {"msg": "Film başarıyla eklendi"}

# === Kullanıcı Oluşturma ===
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

@router.post("/admin/users")
def create_user(user: UserCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password, user_type, is_active)
            VALUES (?, ?, ?, ?,1)
        """, (user.username, user.email, hash_password(user.password), user.role))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Hata: {e}")
    finally:
        conn.close()

    return {"msg": "Kullanıcı başarıyla eklendi"}



# === Rol Güncelleme ===
class RoleUpdate(BaseModel):
    role: str  # "admin" veya "user"

@router.put("/admin/users/{user_id}/role")
def update_user_role(user_id: int, role_update: RoleUpdate):
    if role_update.role not in ("admin", "user"):
        raise HTTPException(status_code=400, detail="Geçersiz rol")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET user_type = ? WHERE id = ?", (role_update.role, user_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        conn.commit()
    finally:
        conn.close()

    return {"msg": "Rol başarıyla güncellendi"}
