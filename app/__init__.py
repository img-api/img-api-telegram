from app.print_helper import *

from imgapi.imgapi import ImgAPI
from imgapi_config import user_config

imgapi = ImgAPI()

print_h1("IMGAPI", "Bot Start")

#imgapi.setup("http://dev.img-api.com:5112/api", {})
imgapi.setup("https://img-api.com/api", {})

user = imgapi.create_user(user_config)