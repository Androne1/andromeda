from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from config import *
from constants import *
from stickers import *



def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up,
        resize_keyboard = True,
        one_time_keyboard = True,
    )
    update.message.reply_text('Добро пожаловать, это список дел')
    update.message.reply_sticker(f'{butler_start}')
    update.message.reply_text('Здесь вы можете создать дело, а также посмотреть, изменить и удалить его или от метить выполненным')
    update.message.reply_text(f'Чтобы начать, нажмите {GO}', reply_markup = keyboard)
    return MENU

def get_menu(update: Update, context: CallbackContext):
    mark_up = [[READ],
               [CREATE, UPDATE],
               [COMPLETE, DELETE]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up,
        resize_keyboard = True,
        one_time_keyboard = True,
    )
    update.message.reply_sticker(menu_sticker)
    update.message.reply_text('Сейчас вы можете выбрать одно из пяти представленных действий', reply_markup = keyboard)
    update.message.reply_text(f'Нажав {READ}, вы увидите ещё не выполненные и не удалённые дела')
    update.message.reply_text(f'Нажав {CREATE}, вы сможете добавить ещё одно дело')
    update.message.reply_text(f'Нажав {UPDATE}, вы сможете изменить одно из уже добавленных дел')
    update.message.reply_text(f'Нажав {COMPLETE}, вы сможете отметить дело, как выполненное, оно будет удалено, а вы получите ещё больше уважения от  меня')
    update.message.reply_text(f'Нажав {DELETE}, вы сможете удалить одно из уже добавленных дел, его отличие от {COMPLETE} состоит в том, что простое удаление дела означает его неактуальность или или невозможность его выполнить, соответственно дпополнительное уважение от меня вы в таком случае не получете, ибо не за что(пожалуйста, используйте эти функции правильно и честно, не люблю обманщиков)')
    
    

def end(update: Update, context: CallbackContext):
    update.message.reply_text("Это конец")
    return ConversationHandler.END