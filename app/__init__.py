from app.print_helper import *

from imgapi.imgapi import ImgAPI
from imgapi_config import user_config

imgapi = ImgAPI()

print_h1("IMGAPI", "Bot Start")

#api.setup("http://img-api.com/api", {})
imgapi.setup("http://dev.img-api.com:5111/api", {})

user = imgapi.create_user(user_config)