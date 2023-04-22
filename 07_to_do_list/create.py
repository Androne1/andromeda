from telegram.ext import (
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackContext
)
from telegram import (
    Update,
    ReplyKeyboardMarkup
)
from start_menu import *
from interrupt import *
from constants import *
from stickers import add_sticker

def add_task(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    update.message.reply_sticker(add_sticker)
    update.message.reply_text(f'Теперь можете добавть дело, {name}')
    return TASK

def handle_task_text(update: Update, context: CallbackContext):
    message = update.message.text
    context.user_data['todo_text'] = message
    update.message.reply_text(message)
    return ConversationHandler.END
    
def endpoint(update: Update, context: CallbackContext):
    update.message.reply_text('Ладно, не будем добавлять дело')
    return ConversationHandler.END

add_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)]
        },
    fallbacks=[CommandHandler('no', endpoint)]
)