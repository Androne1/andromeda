from config import TOKEN
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler
)
from functions import *


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MENU: [MessageHandler(Filters.text & ~Filters.command, get_menu)]
        },
    fallbacks=[CommandHandler('end', end)]
)


dispatcher.add_handler(conv_handler)

print('Сервер запущен!')
updater.start_polling()
updater.idle()  # ctrl + C
