from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import random
import os
from email.mime.text import MIMEText
import smtplib
from backend.models import User, LoginData, Token
from backend.utils import hash_password, verify_password, create_token
from backend.config import DB_PATH

router = APIRouter()

# --- Kayıt için User modeli ---
class SignupUser(BaseModel):
    username: str
    email: str
    password: str
    user_type: str = "user"

# ✉️ Aktivasyon e-postası gönderme (örnek, gerçek SMTP ayarlarını yazman gerek!)

def send_activation_email(to_email, code):
    from email.mime.text import MIMEText
    import smtplib
    import os

    msg = MIMEText(f"Your activation code is: {code}", "plain", "utf-8")
    msg["Subject"] = "Account Activation"
    msg["From"] = os.environ.get("MAILJET_FROM_EMAIL")
    msg["To"] = to_email

    try:
        with smtplib.SMTP("in-v3.mailjet.com", 587) as server:
            server.starttls()
            server.login(
                os.environ.get("MAILJET_API_KEY"),
                os.environ.get("MAILJET_SECRET_KEY")
            )
            server.send_message(msg)
        print("Mail gönderildi!")
    except Exception as e:
        print("SMTP HATASI:", e)




def generate_code(length=6):
    return ''.join(random.choices('0123456789', k=length))



# --- KAYIT OLMA ---
@router.post("/signup")
def signup(user: SignupUser):
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

    cursor.execute("""
        INSERT INTO users (username, password, user_type, email, activation_code, is_active)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (user.username, hashed_pw, user_type, user.email, code, 0)
    )
    conn.commit()
    conn.close()

    send_activation_email(user.email, code)

    return {"message": "Activation code sent to your email."}


# --- HESAP DOĞRULAMA ---
class VerificationData(BaseModel):
    email: str
    code: str

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

# --- GİRİŞ ---
@router.post("/login")
def login(data: LoginData):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, password, user_type, is_active
        FROM users
        WHERE username = ? OR email = ?
    """, (data.username, data.username))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")

    if not verify_password(data.password, row[1]):
        raise HTTPException(status_code=401, detail="Şifre hatalı")

    if row[3] == 0:
        raise HTTPException(status_code=403, detail="Hesap doğrulanmamış. Lütfen e-postanızı kontrol edin.")

    token = create_token(row[0], row[2])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_type": row[2]
    }
