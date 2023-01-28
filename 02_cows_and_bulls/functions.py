from telegram.ext import CallbackContext
from telegram import Update
import random

def game(update: Update, context: CallbackContext):  # callback'
    if 'секретное число' not in context.user_data:
        # если ключа "секретное число" нет в рюкзаке
        secret_number = random.randint(1000, 9999)
        context.user_data['секретное число'] = secret_number
        # создается "секретное число" в рюкзаке
    message = update.message.text
    secret_number = context.user_data['секретное число']  # достаем из рюкзака
    if len(message) != 4 and not message.isdigit():#не число
        update.message.reply_text("Вводить можно только четырехзначные числа!")
        return#выход из функции
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
