from fastapi import APIRouter, HTTPException, Request, Body
from pydantic import BaseModel
from utils import decode_token
from typing import Optional
import sqlite3
import requests
import time
import os

# === Config ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db/movies.db")

# === Router ===
router = APIRouter()

# === Models ===
class Film(BaseModel):
    id: int
    title: str
    year: int
    rating: float
    poster_url: Optional[str] = None

# === Strategy Pattern for Token Decode ===
class TokenDecoder:
    def decode(self, token: str) -> str:
        payload = decode_token(token)
        return payload["sub"]

# === Poster Fetch Strategy ===
class PosterFetcher:
    def fetch(self, title: str) -> str:
        api_key = "729dc000"
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("Poster") and data["Poster"] != "N/A":
                    return data["Poster"]
        except Exception as e:
            print(f"Error fetching poster for {title}: {e}")
        return ""

# === Utilities ===
def get_username_from_token(request: Request) -> str:
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    return TokenDecoder().decode(token)

def get_user_id(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

# === Routes ===
@router.get("/", response_model=list[Film])
def get_all_films():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, year, rating, poster_url FROM films")
    rows = cursor.fetchall()
    conn.close()
    return [Film(id=row[0], title=row[1], year=row[2], rating=row[3], poster_url=row[4]) for row in rows]

@router.get("/{film_id}", response_model=Film)
def get_film_by_id(film_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, year, rating, poster_url FROM films WHERE id = ?", (film_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Film(id=row[0], title=row[1], year=row[2], rating=row[3], poster_url=row[4] or "")
    raise HTTPException(status_code=404, detail="Film not found")

@router.get("/{film_id}/likes")
def get_like_count(film_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM likes WHERE film_id = ?", (film_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return {"count": count}

@router.post("/{film_id}/like")
def like_film(film_id: int, request: Request):
    username = get_username_from_token(request)
    user_id = get_user_id(username)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM likes WHERE user_id = ? AND film_id = ?", (user_id, film_id))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Zaten beğenmişsin")

    cursor.execute("INSERT INTO likes (user_id, film_id) VALUES (?, ?)", (user_id, film_id))
    conn.commit()
    conn.close()
    return {"message": "Film beğenildi"}

@router.get("/{film_id}/average_rating")
def get_average_rating(film_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(score) FROM ratings WHERE film_id = ?", (film_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return {"average": round(result, 1) if result else 0}

@router.post("/{film_id}/rate")
def rate_film(film_id: int, score: int = Body(...), request: Request = None):
    username = get_username_from_token(request)
    user_id = get_user_id(username)

    if not (1 <= score <= 10):
        raise HTTPException(status_code=400, detail="Puan 1 ile 10 arasında olmalı")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ratings WHERE user_id = ? AND film_id = ?", (user_id, film_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE ratings SET score = ? WHERE user_id = ? AND film_id = ?", (score, user_id, film_id))
    else:
        cursor.execute("INSERT INTO ratings (user_id, film_id, score) VALUES (?, ?, ?)", (user_id, film_id, score))

    conn.commit()
    conn.close()
    return {"message": "Puan kaydedildi"}

@router.post("/{film_id}/unlike")
def unlike_film(film_id: int, request: Request):
    username = get_username_from_token(request)
    user_id = get_user_id(username)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM likes WHERE user_id = ? AND film_id = ?", (user_id, film_id))
    conn.commit()
    conn.close()
    return {"message": "Beğeni kaldırıldı"}

@router.get("/{film_id}/user_status")
def get_user_status(film_id: int, request: Request):
    username = get_username_from_token(request)
    user_id = get_user_id(username)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM likes WHERE user_id = ? AND film_id = ?", (user_id, film_id))
    liked = cursor.fetchone() is not None

    cursor.execute("SELECT score FROM ratings WHERE user_id = ? AND film_id = ?", (user_id, film_id))
    score = cursor.fetchone()
    conn.close()

    return {
        "liked": liked,
        "user_score": score[0] if score else None
    }


# === Data Seeder (Builder Pattern-ish) ===
def insert_sample_movies():
    films = [
        ("Inception", 2010, 8.8),
        ("The Matrix", 1999, 8.7),
        ("Interstellar", 2014, 8.6),
        ("The Godfather", 1972, 9.2),
        ("Fight Club", 1999, 8.8),
    ]
    fetcher = PosterFetcher()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM films")

    for i, (title, year, rating) in enumerate(films, start=1):
        print(f"[{i}] Fetching poster for: {title}")
        time.sleep(1)
        poster_url = fetcher.fetch(title)
        cursor.execute("INSERT INTO films (id, title, year, rating, poster_url) VALUES (?, ?, ?, ?, ?)",
                       (i, title, year, rating, poster_url))
    conn.commit()
    conn.close()
    print("✅ Sample films inserted successfully.")

if __name__ == "__main__":
    insert_sample_movies()
