from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.auth import router as auth_router
from backend.film import router as film_router
from backend.comments import router as comments_router
from backend.admin import router as admin_router

app = FastAPI()

import os
from backend.config import DB_PATH


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
app.include_router(admin_router, prefix="/api")

# 🌐 Statik frontend klasörü
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

# Eğer index.html'e özel route vermek istersen:
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
