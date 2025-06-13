from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from film import router as film_router
from comments import router as comments_router

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Gerekirse sadece frontend URL'si ile sınırlandır
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth")
app.include_router(film_router, prefix="/films")
app.include_router(comments_router, prefix="/films")
