import os
import time

from app.bot.bot_telegram import telegram_init
from imgapi_config import telegram_config

from app.print_helper import *
from app import imgapi, user

if 'username' in user:
    print_b("IMGAPI", "TOKEN = " + imgapi.get_token())
    telegram_init(telegram_config, imgapi)
else:
    print_r("IMGAPI", "ERROR: IMG-API.COM failed to provide a token")
