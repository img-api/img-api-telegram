import os
import time

from imgapi_config import telethon_config

from app.print_helper import *
from app import imgapi, user

from app.telethon_bot import telegram_init

if 'username' in user:
    print_b("IMGAPI", "TOKEN = " + imgapi.get_token())
    telegram_init(telethon_config, imgapi)
else:
    print_r("IMGAPI", "ERROR: IMG-API.COM failed to provide a token")
