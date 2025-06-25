import sqlite3
import random
import smtplib
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from email.mime.text import MIMEText
from dotenv import load_dotenv
from models import User, LoginData, Token
from utils import hash_password, verify_password, create_token

# Ortam değişkenlerini yükle
load_dotenv()

router = APIRouter()
DB_PATH = "db/movies.db"

# ✉️ Aktivasyon e-postası gönderme
def send_activation_email(to_email, code):
    msg = MIMEText(f"Your activation code is: {code}")
    msg['Subject'] = 'Account Activation'
    msg['From'] = os.getenv("MAILJET_FROM_EMAIL")
    msg['To'] = to_email

    with smtplib.SMTP_SSL("in-v3.mailjet.com", 465) as server:
        server.login(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_SECRET_KEY"))
        server.send_message(msg)

# 🔑 Aktivasyon kodu oluşturma
def generate_code(length=6):
    return ''.join(random.choices('0123456789', k=length))

# 🧾 Kayıt endpoint'i
@router.post("/signup")
def signup(user: User):
    if not user.username or not user.password or not user.email:
        raise HTTPException(status_code=400, detail="Username, password and email are required")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (user.username, user.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_pw = hash_password(user.password)
    code = generate_code()
    user_type = user.user_type if user.user_type in ("user", "admin") else "user"

    cursor.execute(
        "INSERT INTO users (username, password, user_type, email, activation_code, is_active) VALUES (?, ?, ?, ?, ?, ?)",
        (user.username, hashed_pw, user_type, user.email, code, 0)
    )
    conn.commit()
    conn.close()

    send_activation_email(user.email, code)

    return {"message": "Activation code sent to your email."}

# 📩 Doğrulama veri modeli
class VerificationData(BaseModel):
    email: str
    code: str

# ✅ Doğrulama endpoint'i
@router.post("/verify")
def verify_account(data: VerificationData):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT activation_code FROM users WHERE email = ?", (data.email,))
    row = cursor.fetchone()

    if row and row[0] == data.code:
        cursor.execute("UPDATE users SET is_active = 1 WHERE email = ?", (data.email,))
        conn.commit()
        conn.close()
        return {"message": "Account verified successfully."}
    else:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid verification code")

# 🔓 Giriş endpoint'i
@router.post("/login", response_model=Token)
def login(data: LoginData):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Kullanıcı adı veya e-posta ile giriş yapılabilir
    cursor.execute(
        "SELECT username, password, user_type, is_active FROM users WHERE username = ? OR email = ?",
        (data.username, data.username)
    )
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(data.password, row[1]):
        if row[3] == 0:
            raise HTTPException(status_code=403, detail="Hesap doğrulanmamış. Lütfen e-postanızı kontrol edin.")

        token = create_token(row[0], row[2])
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre.")
