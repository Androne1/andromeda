from config import TOKEN
from telegram.ext import Updater, Filters, MessageHandler
from functions import *




updater = Updater(TOKEN)
dispatcher = updater.dispatcher

game_handler = MessageHandler(Filters.text, game)
dispatcher.add_handler(game_handler)

print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C
