from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    user_type: str


class LoginData(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class Film(BaseModel):
    id: int
    title: str
    year: int