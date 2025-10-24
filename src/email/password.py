import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from fastapi import HTTPException
from src.config import settings
from src.exceptions import IternalServerException
from .utils import get_stmp

SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_EMAIL_PASSWORD = settings.SENDER_EMAIL_PASSWORD

async def send_recovery_code(email: str, recovery_code: str):
    smtp_server, smtp_port = get_stmp(SENDER_EMAIL)

    subject = 'Код восстановления'
    body = f'Ваш код восстановления: <b>{recovery_code:06}<b>'
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg.attach(MIMEText(body, 'html'))

    try:
        await aiosmtplib.send(
            msg,
            hostname=smtp_server,
            port=smtp_port,
            username=SENDER_EMAIL,
            password=SENDER_EMAIL_PASSWORD,
            use_tls=False,
            start_tls=True,  
        )
        return True
    except Exception as e:
        print(f"Ошибка при отправке приглашения: {e}")
        return False