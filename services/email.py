import smtplib
from email.message import EmailMessage
from core.config import settings

async def send_invite_email(to_email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "You're Invited to Faktura"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(f"Click the link to sign up: https://yourdomain.com/signup?token={token}")

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
