from pydantic import BaseModel
from typing import Optional

import os
from backend.config import DB_PATH
class Film(BaseModel):
    id: int
    title: str
    year: int
    rating: float
    poster_url: Optional[str] = None

class User(BaseModel):
    username: str
    password: str
    email: str
    user_type: str = "user"

class LoginData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str
