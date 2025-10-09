import smtplib
from random import randint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import settings
from .utils import get_stmp

SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_EMAIL_PASSWORD = settings.SENDER_EMAIL_PASSWORD

import aiosmtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def send_project_invite(
    recipient_email: str,
    inviter_name: str,
    project_name: str,
    url: str,
) -> bool:
    """
    Асинхронно отправляет приглашение в проект по email
    :param recipient_email: Email получателя
    :param inviter_name: Имя приглашающего
    :param project_name: Название проекта
    :param url: Ссылка для принятия приглашения
    :return: True если отправка успешна, False в случае ошибки
    """
    smtp_server, smtp_port = get_stmp(SENDER_EMAIL)
    
    subject = f"Приглашение в проект {project_name}"
    body = f"""
    <html>
    <body>
        <h2>Вы получили приглашение в проект!</h2>
        <p>{inviter_name} приглашает вас присоединиться к проекту <strong>"{project_name}"</strong>.</p>
        <p>Для принятия приглашения перейдите по ссылке:</p>
        <p><a href="{url}">Принять приглашение</a></p>
        <p>Если вы не ожидали это приглашение, проигнорируйте это письмо.</p>
    </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.attach(MIMEText(body, 'html'))

    try:
        # Асинхронная отправка через aiosmtplib
        await aiosmtplib.send(
            msg,
            hostname=smtp_server,
            port=smtp_port,
            username=SENDER_EMAIL,
            password=SENDER_EMAIL_PASSWORD,
            use_tls=True,
            start_tls=True,  # Включаем STARTTLS
        )
        print(f"Приглашение в проект отправлено на {recipient_email}")
        return True
    except Exception as e:
        print(f"Ошибка при отправке приглашения: {e}")
        return False

