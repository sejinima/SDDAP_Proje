import sqlite3
from fastapi import APIRouter, HTTPException
from models import User, LoginData, Token
from utils import hash_password, verify_password, create_token
from typing import Optional

DB_PATH = "db/movies.db"

router = APIRouter()

@router.post("/signup")
def signup(user: User):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password)
    user_type = user.user_type if user.user_type in ("user", "admin") else "user"

    cursor.execute(
        "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
        (user.username, hashed_pw, user_type)
    )
    conn.commit()
    conn.close()

    token = create_token(user.username, user_type)
    return {"message": "User registered successfully", "access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(data: LoginData):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password, user_type FROM users WHERE username = ?",
        (data.username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(data.password, row[1]):
        token = create_token(row[0], row[2])
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
