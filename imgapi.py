import os
import time

import imgapi_config as cfg

from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Channel, MessageMediaDocument
from telethon.tl.functions.messages import GetHistoryRequest

import imgapi_config as cfg


def ensure_dir(f):
    """Ensure that a needed directory exists, creating it if it doesn't"""
    # print("Ensure dir")
    try:
        d = os.path.dirname(f)
        # print(d)

        if not os.path.exists(d):
            os.makedirs(d)

        return os.path.exists(f)
    except OSError:
        if not os.path.isdir(f):
            raise
    return None

client = TelegramClient('name', cfg.config['API_ID'], cfg.config['API_HASH'])

client.connect()
if not client.is_user_authorized():
    phone_number = cfg.config['PHONE_NUMBER']
    client.send_code_request(phone_number)
    myself = client.sign_in(phone_number, input('Enter code: '))

client.send_message('me', 'Booting system!')

#print(client.download_profile_photo('me', file='data/images/' ))

@client.on(events.NewMessage(pattern='(?i).*Hello'))
async def handler(event):
    await event.reply('Hey!')

oink_channel = client.get_entity('t.me/oinktv')

#client(JoinChannelRequest(oink_channel))

found_media = {}

offset = 0

b_exit = False
limit = 10

data_folder = "data/"
channel_name = "oinktv"

channel_folder = "data/" + channel_name
ensure_dir(channel_folder)

while not b_exit:
    messages = client.get_messages(oink_channel, limit=limit, add_offset=offset)
    for msg in reversed(messages):
        # Format the message content

        # offset_id=full_msg_list[-1].id\

        if getattr(msg, 'media', None):
            print(str(msg.date) + " Found media id " + str(msg.id))

            found_media[msg.id] = msg

            media_folder = channel_folder + "/" + str(msg.id) + "/"
            if os.path.exists(media_folder):
                print(" Found folder " + media_folder)
                continue

            ensure_dir(media_folder)

            media = msg.media
            mime = media.document.mime_type.lower()

            # Get the maximum size thumb
            # client.download_media(msg, media_folder, thumb=-1)

            print("+  Media " + mime)
            client.download_media(msg, media_folder)
            content = '<{}> {}'.format(
                type(msg.media).__name__, msg.message)

        elif hasattr(msg, 'message'):
            content = msg.message
        elif hasattr(msg, 'action'):
            content = str(msg.action)
        else:
            # Unknown message, simply print its class name
            content = type(msg).__name__

        time.sleep(5)

    offset += limit
    time.sleep(5)

    #client.run_until_disconnected()