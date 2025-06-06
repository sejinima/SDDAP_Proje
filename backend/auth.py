from fastapi import APIRouter, HTTPException
from models import User, LoginData, Token
from utils import hash_password, verify_password, create_token
from typing import List

router = APIRouter()
user_db: List[User] = []


@app.post("/signup")
def signup(user: User):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Sabit user_type: user
    cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", 
                   (user.username, user.password, "user"))
    conn.commit()
    conn.close()
    
    return {"message": "User registered successfully"}


@router.post("/login", response_model=Token)
def login(data: LoginData):
    for u in user_db:
        if u.username == data.username and verify_password(data.password, u.password):
            token = create_token(u.username, u.user_type)
            return{"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials") 