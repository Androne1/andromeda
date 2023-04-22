from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update
from stickers import bullshit_sticker
from config import *


def end(update: Update, context: CallbackContext):
    update.message.reply_text("Это конец")
    return ConversationHandler.END

def fool_protection(update: Update, context: CallbackContext):
    update.message.reply_sticker(bullshit_sticker)
    update.message.reply_text('Что бы это ни было, я такого не умею')