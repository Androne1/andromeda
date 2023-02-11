from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random

BEGIN, LEVEL, GAME = 1, 2, 3
GO = 'Вперёд'
EASY, MEDIUM, HARD = 'простой', 'средний', 'сложный'

def start(update: Update, context: CallbackContext):
    button = [[GO]]
    keyboard = ReplyKeyboardMarkup(button, resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder=f'Нажми на кнопку {GO}')
    update.message.reply_text(
        'В этой игре загадывается число, которое ты должен отгадать, из этого слова тебе известно только количество букв')
    update.message.reply_text(
        'Ты пишешь слово из такого же количества букв, если и в твоём слове, и в загаданном одна и та же буква находится на одном и том же месте, то я скажут тебе, что в твоём слове один бык'
    )
    update.message.reply_text(
        'Если совпадает только буква, но не её расположение, то я скажу тебе, что в слове одна корова'
    )
    update.message.reply_text(
        'Количество быков и коров будет меняться в соответствии с указанными параметрами'
    )
    update.message.reply_text(
        'Игра закончится, когда слово будет отгадано'
    )
    update.message.reply_text(
        f'Чтобы играть, нажми "{GO}"', reply_markup = keyboard
    )
    update.message.reply_text(
        'Ты всегда можешь выйти из игры, для этого нажми /end'
        )
    return BEGIN # переход к следующему шагу

def begin (update: Update, context: CallbackContext):
    mark_up = [[EASY],
               [MEDIUM],
               [HARD]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up, 
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Выбери уровень сложности: {EASY} - 3 буквы, {MEDIUM} - 4 буквы, {HARD} - 5 букв'
    )
    # если ключа "секретное число" нет в рюкзаке
    secret_number = random.randint(1000, 9999)
    context.user_data['секретное число'] = secret_number
    # создается "секретное число" в рюкзаке
    update.message.reply_text('Число загадано, теперь попытайся отгадать его')
    return GAME

def game(update: Update, context: CallbackContext):  # callback'
    message = update.message.text
    secret_number = context.user_data['секретное число']  # достаем из рюкзака
    if len(message) != 4 and not message.isdigit():#не число
        update.message.reply_text("Вводить можно только четырехзначные числа!")
        return # выход из функции
    cows = 0
    bulls = 0
    secret_number = str(secret_number)
    for mesto, chislo in enumerate(message):
        if chislo in secret_number:
            if message[mesto] == secret_number[mesto]:
                bulls += 1
            else:
                cows += 1
    update.message.reply_text(f'В вашем числе {cows} коров и {bulls} быков')
    if bulls == 4:
        update.message.reply_text('Вы угадали! Вы красавчик')
        del context.user_data['секретное число']

def end(update: Update, context: CallbackContext):
    update.message.reply_text('Значит, ты выбрал конец')
    return ConversationHandler.END