from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random
import pymorphy2
from stickers import *


morph = pymorphy2.MorphAnalyzer()
BEGIN, GET_NAME, LEVEL, GAME = range(4)
GO = "Вперед"
SKIP = "Пропустить"
GIVE_UP = "Сдаться"
EASY, MEDIUM, HARD = "Простой", "Средний", "Сложный"


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up,
        resize_keyboard = True,
        one_time_keyboard = True,
        input_field_placeholder = f'Нажми на кнопку "{GO}", поиграем!'
    )
    update.message.reply_sticker(start_sticker)
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
    update.message.reply_sticker(go_sticker)
    return GET_NAME

def get_name(update: Update, context: CallbackContext):
    mark_up = [[SKIP]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up,
        resize_keyboard = True,
        one_time_keyboard = True)
    full_name = update.effective_chat.full_name
    update.message.reply_text(f"Можно называть вас {full_name}? Если нет, то ведите своё имя имя, иначе нажмите {SKIP}", reply_markup = keyboard)
    update.message.reply_sticker(question_sticker)
    return BEGIN

def begin(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data ['tries'] = 0
    if name == SKIP:
        name = update.effective_chat.full_name
    context.user_data["username"] = name
    mark_up = [[EASY, MEDIUM, HARD]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'{EASY} - 3 буквы, {MEDIUM} - 4 буквы, {HARD} - 5 букв'
    )
    update.message.reply_text(f'А теперь, {name}, выбери уровень сложности или нажми /end!', reply_markup=keyboard)
    
    
    # если ключа "секретное число" нет в рюкзаке
    # secret_number = random.randint(1000, 9999)
    # context.user_data['секретное число'] = secret_number
    # update.message.reply_text('Я загадал число, отгадай или нажми /end!')
    # создается "секретное число" в рюкзаке
    return LEVEL


def level (update: Update, context: CallbackContext):
    level_storage = update.message.text
    name = context.user_data["username"]
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
        update.message.reply_text(f'{name}, этот файл недоступен')
    word = random.choice(words)
    context.user_data['secret_slovo'] = word
    update.message.reply_text(f'Я загадал слово, а теперь, {name}, отгадайте его, оно состоит из {len(word)} букв')
    return GAME


def game(update: Update, context: CallbackContext):  # callback'
    mark_up = [[GIVE_UP]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up,
        resize_keyboard = True,
        one_time_keyboard = True
    )
    if context.user_data ['tries'] == 0:
        update.message.reply_text('Если ты хочешь прекратить попытки отгадать слово, нажми Сдаться', reply_markup = keyboard)
    context.user_data['tries'] += 1
    secret_word = context.user_data['secret_slovo']  # достаем из рюкзака
    if context.user_data['tries'] >= 3:
        letters = list(secret_word)
        one_letter = random.choice(letters)
        update.message.reply_text = f'В слове есть буква {one_letter}'
    my_word = update.message.text.lower()
    if my_word == 'сдаться':
        update.message.reply_text(f'Вы не смогли угадать слово {secret_word}')
        return ConversationHandler.END
    tag = morph.parse(my_word)[0]
    if len(my_word) != len(secret_word) and my_word.isalpha:  # не число
        update.message.reply_text(f"Нужно вводить слова из {len(secret_word)} букв")
        return  # выход из функции
    elif my_word != tag.normal_form or tag.tag.POS != 'NOUN':
        print(tag)
        update.message.reply_text('Нужно вводить существительные в начальной форме, которые есть в словаре русского языка')
        return
    cows = 0
    bulls = 0
    for mesto, letter in enumerate(my_word):
        if letter in secret_word:
            if my_word[mesto] == secret_word[mesto]:
                bulls += 1
            else:
                cows += 1
    update.message.reply_text(f'В вашем слове {cows} коров и {bulls} быков')
    if bulls == len(secret_word):
        update.message.reply_text('Вы угадали! Вы красавчик')
        update.message.reply_text('Чтобы начать заново нажмите /end, а затем /start')
        del context.user_data['secret_slovo']


def end(update: Update, context: CallbackContext):  # точка выхода
    name = context.user_data["username"]
    update.message.reply_text(f"Это конец, {name}")
    return ConversationHandler.END