from fastapi import APIRouter, HTTPException
from models import User, LoginData, Token
from utils import hash_password, verify_password, create_token
from typing import List

router = APIRouter
user_db: List[User] = []

@router.post("/signup")
def signup(user: User):
    for u in user_db:
        if u.username == user.username:
            raise HTTPException(status_code=400, detail) = "Username already exists")

    user.password = hash_password(user.password)
    user_db.append(user)
    return {"message": "User created"}

@router.post("/login", response_model=Token)
def login(data: LoginData):
    for u in user_db:
        if u.username == data.username and verify_password(data.password, u.password):
            token = create_token(u.username, u.user_type)
            return{"access_token": token, "token_type": "bearer"}
       raise HTTPException(status_code=401, detail="Invalid credentials") 