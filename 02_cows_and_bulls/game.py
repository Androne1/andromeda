from config import TOKEN
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, ConversationHandler
from functions import *


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        BEGIN: [MessageHandler(Filters.text & ~Filters.command, begin)],
        GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
    },
    fallbacks=[CommandHandler('end', end)]
    )

dispatcher.add_handler(conv_handler)

print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C