import smtplib
from email.mime.text import MIMEText

api_key = "07a6503ff1ecd797116644f02f7c21d7"
secret_key = "72760fb13c16118c56ce307aae6653b8"
from_mail = "trkhsmlr77@gmail.com"
to_mail = "5091c53443@emaily.pro"

msg = MIMEText("mailjet test: gusioc", "plain", "utf-8")
msg["Subject"] = "mailjet test: sg"
msg["From"] = from_mail
msg["To"] = to_mail

try:
    with smtplib.SMTP("in-v3.mailjet.com", 587) as server:
        server.starttls()
        server.login(api_key, secret_key)
        server.send_message(msg)

    print("Mail gönderildi!")
except Exception as e:
    print("SMTP HATASI:", e)
