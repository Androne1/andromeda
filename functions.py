from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random


BEGIN, LEVEL, GAME = range(3)
GO = "Вперед"
EASY, MEDIUM, HARD = "Простой", "Средний", "Сложный"


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", поиграем!'
    )
    update.message.reply_text(
        'В этой игре компьютер загадывает слово, и говорит тебе, сколько в нем букв')
    update.message.reply_text('Ты говоришь слово из такого же количества букв')
    update.message.reply_text(
        'Если у какой-то из букв твоего совпадает позиция с буквой из загаданного слова - это бык')
    update.message.reply_text(
        'Если просто такая буква есть в слове - это корова')
    update.message.reply_text("Твоя цель - отгадать загаданное слово")
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)
    return BEGIN


def begin(update: Update, context: CallbackContext):
    mark_up = [[EASY, MEDIUM, HARD]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'{EASY} - 3 буквы, {MEDIUM} - 4 буквы, {HARD} - 5 букв'
    )
    update.message.reply_text('Выбери уровень сложности или нажми /end!', reply_markup=keyboard)
    
    
    # если ключа "секретное число" нет в рюкзаке
    # secret_number = random.randint(1000, 9999)
    # context.user_data['секретное число'] = secret_number
    # update.message.reply_text('Я загадал число, отгадай или нажми /end!')
    # создается "секретное число" в рюкзаке
    return LEVEL


def level (update: Update, context: CallbackContext):
    level_storage = update.message.text
    if level_storage == EASY:
        with open('02_cows_and_bulls/easy.txt', encoding = 'utf-8') as file:
            words = file.read().split('\n')
    elif level_storage == MEDIUM:
        with open('02_cows_and_bulls/medium.txt', encoding = 'utf-8') as file:
            words = file.read().split('\n')
    elif level_storage == HARD:
        with open('02_cows_and_bulls/hard.txt', encoding = 'utf-8') as file:
            words = file.read().split('\n')
    else:
        update.message.reply_text('Файл недоступен')
    word = random.choice(words)
    context.user_data['secret_slovo'] = word
    update.message.reply_text(f'Было выбрано слово слово {word}')
    return GAME


def game(update: Update, context: CallbackContext):  # callback'
    message = update.message.text
    secret_number = context.user_data['секретное число']  # достаем из рюкзака
    if len(message) != 4 and not message.isdigit():  # не число
        update.message.reply_text("Вводить можно только четырехзначные числа!")
        return  # выход из функции
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

def end(update: Update, context: CallbackContext):  # точка выхода
    update.message.reply_text("Значит, ты выбрал конец")
    return ConversationHandler.END