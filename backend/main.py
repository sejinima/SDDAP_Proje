from fastapi import FastAPI
from auth import router as auth_router
from film import router as film_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(film_router, prefix="/film")