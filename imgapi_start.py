import os
import time

from imgapi.imgapi import ImgAPI
from app.print_helper import *

from imgapi_config import user_config, telegram_config
from app.bot.bot_telegram import telegram_init

api = ImgAPI()

print_h1("IMGAPI", "Bot Start")

#api.setup("http://img-api.com/api", {})
api.setup("http://dev.img-api.com:5111/api", {})

user = api.create_user(user_config)

if 'username' in user:
    print_b("IMGAPI", "TOKEN = " + api.get_token())
    telegram_init(telegram_config, api)
else:
    print_r("IMGAPI", "ERROR: IMG-API.COM failed to provide a token")
