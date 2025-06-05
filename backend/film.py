from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import requests
import time

router = APIRouter()
DB_PATH = "db/movies.db"

class Film(BaseModel):
    id: int
    title: str
    year: int
    rating: float
    poster_url: str

def fetch_image_url(title: str) -> str:
    api_key = "729dc000"  # OMDb API key
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

@router.get("/", response_model=List[Film])
def get_all_films():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, year, rating, poster_url FROM films")
    rows = cursor.fetchall()
    conn.close()
    films = [Film(id=row[0], title=row[1], year=row[2], rating=row[3], poster_url=row[4]) for row in rows]
    return films

@router.get("/{film_id}", response_model=Film)
def get_film_by_id(film_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, year, rating, poster_url FROM films WHERE id = ?", (film_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Film(id=row[0], title=row[1], year=row[2], rating=row[3], poster_url=row[4])
    else:
        raise HTTPException(status_code=404, detail="Film not found")

def insert_sample_movies():
    films = [
        ("Inception", 2010, 8.8),
        ("The Matrix", 1999, 8.7),
        ("Interstellar", 2014, 8.6),
        ("The Godfather", 1972, 9.2),
        ("Fight Club", 1999, 8.8),
    ]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM films")
    for i, (title, year, rating) in enumerate(films, start=1):
        print(f"[{i}] Fetching poster for: {title}")
        time.sleep(1)  # Sunucuyu yormamak için
        poster_url = fetch_image_url(title)
        cursor.execute("""
            INSERT INTO films (id, title, year, rating, poster_url)
            VALUES (?, ?, ?, ?, ?)
        """, (i, title, year, rating, poster_url))
    conn.commit()
    conn.close()
    print("✅ Sample films inserted successfully.")

if __name__ == "__main__":
    insert_sample_movies()
