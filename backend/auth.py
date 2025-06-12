import sqlite3
from fastapi import APIRouter, HTTPException
from models import User, LoginData, Token
from utils import hash_password, verify_password, create_token
from typing import List

DB_PATH = "db/movies.db"

router = APIRouter()

@router.post("/signup")
def signup(user: User):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Aynı kullanıcı adı varsa hata ver
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    # Şifreyi hashle
    hashed_pw = hash_password(user.password)

    # Kullanıcıyı "user" tipiyle ekle
    cursor.execute(
        "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
        (user.username, hashed_pw, "user")
    )
    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(data: LoginData):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Kullanıcıyı al
    cursor.execute(
        "SELECT username, password, user_type FROM users WHERE username = ?",
        (data.username,)
    )
    row = cursor.fetchone()
    conn.close()

    # Kullanıcı varsa ve şifre doğruysa token döndür
    if row and verify_password(data.password, row[1]):
        token = create_token(row[0], row[2])
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
