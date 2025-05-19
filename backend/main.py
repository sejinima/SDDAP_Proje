from fastapi import FastAPI
from auth import router as auth_router
from film import router as film_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # veya sadece "http://localhost:8080"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(film_router, prefix="/film")