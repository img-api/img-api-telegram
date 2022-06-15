import os
import hashlib
import datetime

from app.print_helper import *

print_h1("BOT", "Telegram Instance")

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    RegexHandler,
    CallbackQueryHandler,
)

from app.print_helper import *
import os

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep

telegram_bot = None
imgapi = None
config = None

galleries = {}
def get_gallery(update, context):
    tid = update.effective_chat.id
    if tid in galleries:
        return galleries[tid]

    gallery_def = {
        "my_telegram_id": update.effective_chat.id,
        "title": update.effective_chat.title
    }

    galleries[tid] = imgapi.create_gallery(gallery_def)

def coms_send_notification(chat_id,
                           text,
                           id=-1,
                           parse_mode=telegram.ParseMode.HTML):
    global telegram_bot
    try:
        telegram_bot.send_message(chat_id=chat_id,
                                  text=text,
                                  parse_mode=parse_mode)
    except Exception as err:
        print(str(err))
        return


def start(update, context):
    """Send a message when the command /start is issued."""

    coms_send_notification(
        update.effective_chat.id,
        '\n\nHi, Welcome to <i>Img-api.com</i> gallery system\n Type /help to get more help and a commands list!\n Invite me to a channel to create a new Gallery'
    )


def help(update, context):
    """Send a message when the command /help is issued."""

    coms_send_notification(
        update.effective_chat.id,
        '\n\n<b>Help!</b>\n' + "/report <b>1</b> Send report \n")


def echo(update=None, context=None, Test=None):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    print_alert(str(context.error))

    coms_send_notification(update.effective_chat.id,
                           "Error " + str(context.error))
    return


def report(update, context):
    tmp = " <b>Report</b><pre>\n"
    tmp += "-----------------------------------------------------\n"
    tmp += "</pre>\n"

    coms_send_notification(update.effective_chat.id, tmp)
    return


def text_event(update, context):
    user = update.message.from_user
    update.effective_chat.title

    last_comment = update.message.text
    print_b(update.effective_chat.title, user.id, update.message.text)
    gallery = get_gallery(update, context)


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    global imgapi

    chat_id = update.effective_chat.id
    # img-api get gallery from id

    user = update.message.from_user
    photo = update.message.photo[-1]
    photo_file = photo.get_file()

    # Save as temporal so we can get the MD5
    tmp_file = 'content/tmp_upload.jpg'
    ensure_dir(tmp_file)
    photo_file.download(tmp_file)

    with open(tmp_file, 'rb') as fp:
        md5 = hash_bytestr_iter(file_as_blockiter(fp), hashlib.md5(), True)

    # Save as it's final name
    year = datetime.datetime.today().year
    folder = "content/" + str(year) + "/"
    ensure_dir(folder)

    media_file_name = folder + md5 + ".jpg"

    reply = 'Photo saved.\n'
    try:
        stat = os.stat(media_file_name)
        file_size = stat.st_size
        reply = "------------------------------------\n WARNING: File already exists \n------------------------------------\n"
    except Exception as e:
        pass

    print_h1("SAVED PHOTO " + str(media_file_name))
    photo_file.download(media_file_name)

    try:
        json_res = imgapi.api_upload([media_file_name])
    except Exception as e:
        print(" Fialed creating user ")

    os.remove(media_file_name)
    return 1


def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()


def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

    return os.path.exists(f)


def video(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user

    video = update.message.video
    if not video:
        # We have a gif comming
        video = update.message.document

    video_file = video.get_file()

    # Save as temporal so we can get the MD5
    tmp_file = 'content/tmp_upload.mp4'
    ensure_dir(tmp_file)
    video_file.download(tmp_file)

    with open(tmp_file, 'rb') as fp:
        md5 = hash_bytestr_iter(file_as_blockiter(fp), hashlib.md5(), True)

    # Save as it's final name
    year = datetime.datetime.today().year
    folder = "content/" + str(year) + "/"
    ensure_dir(folder)

    media_file_name = folder + md5 + ".mp4"

    reply = 'Video saved.\n'
    try:
        stat = os.stat(media_file_name)
        file_size = stat.st_size
        reply = "------------------------------------\n WARNING: File already exists \n------------------------------------\n"
    except Exception as e:
        pass

    print_h1("SAVED VIDEO " + str(media_file_name))

    video_file.download(media_file_name)

    os.remove(media_file_name)

    try:
        json_res = imgapi.api_upload([media_file_name])
    except Exception as e:
        print(" Fialed creating user ")

    return 1


def group_hook(update, context):
    msg = update.effective_message

    #if msg.group_chat_created:
    #    self.bus.post(GroupChatCreatedEvent(chat_id=update.effective_chat.id,
    #                                        message=self._plugin.parse_msg(msg).output,


def telegram_loop():
    global telegram_bot
    global config

    updater = Updater(config["token"], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("report", report))

    #dp.add_handler(MessageHandler(Filters.chat_type.groups, group_hook))
    dp.add_handler(MessageHandler(Filters.text, text_event))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    dp.add_handler(MessageHandler(Filters.video, video))
    dp.add_handler(MessageHandler(Filters.document.gif, video))
    dp.add_handler(MessageHandler(Filters.regex('^(/report_[\d]+)$'), report))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    telegram_bot = updater.bot


def echo(bot):
    # Request updates after the last update_id
    update_id = 0
    for update in bot.get_updates(offset=update_id, timeout=1):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)


def telegram_init(cfg, api):
    global imgapi
    global config

    config = cfg
    imgapi = api

    # Telegram Bot Authorization Token
    if "token" not in config:
        return

    if config["token"] == None or len(config["token"]) == 0:
        print_alert("", "Token not found")
        return

    telegram_loop()
