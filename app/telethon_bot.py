import os
import time

from .print_helper import *

from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Channel, MessageMediaDocument
from telethon.tl.functions.messages import GetHistoryRequest

from app.file_helper import ensure_dir

galleries = {}

def get_gallery(imgapi, update):
    tid = update.effective_chat.id
    if tid in galleries:
        return galleries[tid]

    gallery_def = {
        "my_telegram_id": update.effective_chat.id,
        "title": update.effective_chat.title,
        "is_public": True,
    }

    json = imgapi.create_gallery(gallery_def)

    if 'galleries' in json:
        gallery = json['galleries'][0]
        galleries[tid] = gallery
        print_b('BOT', " Gallery " + gallery['name'])
        return gallery

    return None


def get_gallery_id(imgapi, update):
    gallery = get_gallery(imgapi, update)
    gid = gallery and gallery['id'] if 'id' in gallery else None
    return gid


def telegram_init(cfg, imgapi):
    client = TelegramClient('name', cfg['API_ID'], cfg['API_HASH'])

    client.connect()
    if not client.is_user_authorized():
        phone_number = cfg['PHONE_NUMBER']
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
        messages = client.get_messages(oink_channel,
                                       limit=limit,
                                       add_offset=offset)
        for msg in reversed(messages):
            # Format the message content

            # offset_id=full_msg_list[-1].id\

            if getattr(msg, 'media', None):
                print(str(msg.date) + " Found media id " + str(msg.id))

                found_media[msg.id] = msg

                media_folder = channel_folder + "/" + str(msg.id) + "/"
                if os.path.exists(media_folder):
                    print(" Found folder " + media_folder)
                    time.sleep(1)
                    continue

                ensure_dir(media_folder)
                media = msg.media

                try:
                    mime = media.document.mime_type.lower()
                    path = client.download_media(msg, media_folder)

                    print("+ Media: " + mime)
                    print("+ Path: " + path)

                    res = imgapi.api_check_md5(path)
                    if not 'media_files' in res:
                        print_b("Upload")
                        json_res = imgapi.api_upload([path], gallery_id=None)
                    else:
                        print_r("Duplicated")

                    os.remove(path)

                except Exception as e:
                    print(" Fialed uploading video ")

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
