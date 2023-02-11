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
    states = {
        EAT: [MessageHandler(Filters.text & ~Filters.command, what_eating)],
        DRINK:[MessageHandler(Filters.text & ~Filters.command, what_drinking)],
        OLD: [MessageHandler(Filters.text & ~Filters.command, how_old)]
    },
    fallbacks=[CommandHandler('cancel',cancel)]
    
)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(dialog_handler)



print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C