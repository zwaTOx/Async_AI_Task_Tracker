import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from src.config import settings
from src.exceptions import IternalServerException
from .utils import get_stmp

SENDER_EMAIL = settings.SENDER_EMAIL

def send_recovery_code(email: str, recovery_code: str):
    smtp_server, smtp_port = get_stmp(SENDER_EMAIL)

    subject = 'Код восстановления'
    body = f'Ваш код восстановления: <b>{recovery_code:06}<b>'
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=120) as host:
            host.starttls()
            host.login(SENDER_EMAIL, settings.SENDER_EMAIL_PASSWORD)
            host.sendmail(SENDER_EMAIL, email, msg.as_string())
        print("Код восстановления отправлен на", email)
    except Exception as e:
        raise IternalServerException(detail="Ошибка отправки кода на почту")
    return recovery_code