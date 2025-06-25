from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from auth import router as auth_router
from film import router as film_router
from comments import router as comments_router
from backend.admin import router as admin_router


app = FastAPI()

# 🔓 CORS ayarları (Geliştirme aşamasında her şeye izin verebiliriz)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için tüm kaynaklara izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 API router'ları
app.include_router(auth_router, prefix="/auth")
app.include_router(film_router, prefix="/films")
app.include_router(comments_router, prefix="/films")
app.include_router(admin_router, prefix="/api")


# 🌐 Frontend dizinini tanımla
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

# 📁 HTML, CSS, JS dosyaları için statik servis
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

# 🔗 Ana sayfa (opsiyonel, index.html doğrudan serve edilir)
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
