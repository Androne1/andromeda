from config import TOKEN
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    ConversationHandler,
    CommandHandler
    )

from functions import *


dialog_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST_NAME:[MessageHandler(Filters.text & ~Filters.command, get_name)],
        LAST_NAME:[MessageHandler(Filters.text & ~Filters.command, get_surname)],
        PATER_NAME:[MessageHandler(Filters.text & ~Filters.command, get_patername)],
    },
    fallbacks=[CommandHandler('end',end)]
    
)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(dialog_handler)



print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C
