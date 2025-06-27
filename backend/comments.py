import sqlite3
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List
from datetime import datetime

from backend.utils import decode_token
from backend.config import DB_PATH

router = APIRouter()

# 🗨️ Yorum modeli (timestamp artık otomatik atanıyor, dışarıdan alınmıyor)
class Comment(BaseModel):
    text: str

# 🔓 Token'dan kullanıcı adı çıkar
class TokenDecoder:
    def decode(self, token: str) -> str:
        payload = decode_token(token)
        return payload["sub"]

def get_username_from_token(request: Request) -> str:
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    return TokenDecoder().decode(token)

# 💬 Yorum ekleme
@router.post("/{film_id}/comment")
def add_comment(film_id: int, comment: Comment, request: Request):
    username = get_username_from_token(request)
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO comments (film_id, username, text, timestamp)
        VALUES (?, ?, ?, ?)
    """, (film_id, username, comment.text, timestamp))
    conn.commit()
    conn.close()

    return {"message": "Comment added successfully"}

# 📄 Yorumları listeleme
@router.get("/{film_id}/comments", response_model=List[dict])
def get_comments(film_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, text, timestamp
        FROM comments
        WHERE film_id = ?
        ORDER BY timestamp DESC
    """, (film_id,))
    rows = cursor.fetchall()
    conn.close()

    return [{"username": row[0], "text": row[1], "timestamp": row[2]} for row in rows]
