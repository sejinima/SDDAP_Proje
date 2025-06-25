from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from auth import router as auth_router
from film import router as film_router
from comments import router as comments_router

app = FastAPI()

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 API router'ları
app.include_router(auth_router, prefix="/auth")
app.include_router(film_router, prefix="/films")
app.include_router(comments_router, prefix="/films")

# 🌐 Statik frontend klasörü
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

# Ana sayfayı manuel route ile göstermek istersen:
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
