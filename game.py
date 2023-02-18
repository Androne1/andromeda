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
          BEGIN: [MessageHandler(Filters.regex(f'^({GO})$'), begin)],
          LEVEL: [MessageHandler(Filters.regex(f'^({EASY}|{MEDIUM}|{HARD})$'), level)],
          GAME: [MessageHandler(Filters.text & ~Filters.command, game)]  
        },
    fallbacks=[CommandHandler('end', end)]
)


dispatcher.add_handler(conv_handler)

print('Сервер запущен!')
updater.start_polling()
updater.idle()  # ctrl + C
