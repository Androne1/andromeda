from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update

FIRST_NAME, LAST_NAME, PATER_NAME = 1, 2, 3


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Разговор начался. Давайте соберем данные о Вас.")
    update.message.reply_text("Назови мне своё имя.")
    return FIRST_NAME


def get_name(update: Update, context: CallbackContext):
    name = update.message.text # берем сообщение, которое ввели
    context.user_data['name'] = name  # сохранили имя в рюкзаке
    update.message.reply_text(f"Вы ввели имя {name}")
    update.message.reply_text("Назови мне свою фамилию.")
    return LAST_NAME

def get_surname(update: Update, context: CallbackContext):
    last_name = update.message.text # берем сообщение, которое ввели
    context.user_data['last_name'] = last_name  # сохранили имя в рюкзаке
    update.message.reply_text(f"Вы ввели фамилию {last_name}")
    update.message.reply_text("Введите отчество")
    return PATER_NAME

def get_patername(update: Update, context: CallbackContext):
    patername = update.message.text # берем сообщение, которое ввели
    context.user_data['patername'] = patername  # сохранили имя в рюкзаке
    name = context.user_data['name']
    last_name = context.user_data['last_name']
    
    context.user_data['user'] = f"{patername} {name} {last_name}"
    
    update.message.reply_text(f"Да вы у нас {patername} {name} {last_name}, я гляжу!")
    update.message.reply_text("Введите ваш возраст")
    return ConversationHandler.END

def get_age(update: Update, context: CallbackContext):
    age = update.message.text
    if age.isdigit() == False:
        update.message.reply_text("Вы ввели не число ")



def end(update: Update, context: CallbackContext):
    update.message.reply_text("Сбор данных прерван")
    return ConversationHandler.END