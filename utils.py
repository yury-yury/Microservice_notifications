import random

import smtplib
from typing import List

from settings import settings


async def send_email(from_addr: str, to_addr: str, subject: str, msg: str) -> bool:
    """
    The asynchronous send_email function is designed to send notifications to users.
    Takes the following mandatory positional arguments as parameters:
        the email from which the mailing will be sent,
        the email address of the recipient to whom the notifications will be sent,
        the text of the notification header and
        the text of the notification context.
    All arguments are accepted as strings.
    Returns the result of sending a notification in the form True if the sending is successful,
    otherwise False.
    """
    try:
        server = smtplib.SMTP(f'{settings.SMTP_HOST}:{settings.SMTP_PORT}')
        server.ehlo()
        server.starttls()
        server.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
        message = f'Subject: {subject}\n\n{msg}'
        server.sendmail(from_addr, to_addr, message)
        server.quit()

    except Exception:
        print("Error sending letter!")
        return False

    else:
        return True


async def get_random_number(n: int = 24) -> str:
    """
    The get_random_number asynchronous function is designed to generate a random entity ID.
    Takes as an argument an optional parameter corresponding to the length of the character sequence.
    By default - 24 characters. Returns the generated sequence as a string.
    """
    list_character: List[str] = list('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
    res: str = str()
    for _ in range(n):
        res += random.choice(list_character)
    return res
