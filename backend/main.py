from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Geçici film verisi (ileride database bağlayacağız)
class Film(BaseModel):
    id: int
    title: str
    year: int

films = [
    Film(id=1, title="The Matrix", year=1999),
    Film(id=2, title="Inception", year=2010),
    Film(id=3, title="Parasite", year=2019)
]

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

@app.get("/films", response_model=List[Film])
def get_films():
    return films
