from config import TOKEN
from telegram.ext import Updater, CommandHandler,CallbackContext, MessageHandler, Filters
from telegram import Update
from anecAPI import anecAPI


def hello(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    update.message.reply_animation('https://acegif.com/wp-content/uploads/gifs/privet-47.gif')
    update.message.reply_text(f'Привет, {name}!')

def start(update: Update, context: CallbackContext):
    update.message.reply_text('''Меня зовут Леонид. Я знаю команды: 
    /hello - Приветствие
    /bye - Прощание
    /contact - Отправлю контакт
    /echo - Повторю твои слова
    ''')


def bye(update: Update, context: CallbackContext):
    name = update.effective_user.full_name
    context.bot.send_photo(update.effective_chat.id,'https://tlgrmx.ru/stickers/2641/41.png')
    context.bot.send_message(update.effective_chat.id,f'Пока, {name}!')

def send_contact(update: Update, context: CallbackContext):
    update.message.reply_contact('88005553535', 'Илон','Маск')
    
def echo(update: Update, context: CallbackContext):
    args = context.args
    text = ' '.join(args)#объединили список
    if text == '':
        update.message.reply_text('Введите слово после команды /echo')
    else:
        update.message.reply_text(text)


def is_number(num, update):
    try: #попытайся выполнить этот код
        num = int(num)#преврати в число
        return num
    except ValueError:#если поймаешь ошибку ValueError
        update.message.reply_text('Вы ввели не число')
        return None
 
def get_numbers(update: Update, context: CallbackContext):       
    args = context.args # два числа 
    if len(args) != 2:# != - это неравно
        update.message.reply_text('Вы можете ввести только два числа')
        return False
    num1 = is_number(args[0], update) # берем первое число
    num2 = is_number(args[1], update) if num1 else None# берем второе число
    if not num1 or not num2:
        return False
    return num1, num2
    

def plus(update: Update, context: CallbackContext):
    if get_numbers(update,context):#если не False
        num1, num2 = get_numbers(update,context)#два числа записываются в две переменные
        result = num1 + num2 # складываем числа
        update.message.reply_text(result) # выводим в мессенджер
    

def minus(update: Update, context: CallbackContext):
    if get_numbers(update,context):#если не False
        num1, num2 = get_numbers(update,context)
        result = num1 - num2 # складываем числа
        update.message.reply_text(result) # выводим в мессенджер

def div(update: Update, context: CallbackContext):
    if get_numbers(update,context):#если не False
        num1, num2 = get_numbers(update,context)
        result = num1 / num2 # складываем числа
        update.message.reply_text(result) # выводим в мессенджер

def mult(update: Update, context: CallbackContext):
    if get_numbers(update,context):#если не False
        num1, num2 = get_numbers(update,context)
        result = num1 * num2 # складываем числа
        update.message.reply_text(result) # выводим в мессенджер    
        
def make_jokes(update: Update, context: CallbackContext):
    message = update.message.text
    if 'штирлиц' in message.lower():
        update.message.reply_text(f'Штирлиц топил камин. Камин утонул.')
    elif 'бэтмен' in message.lower():
        update.message.reply_text(f'i am the vengeance. i am the night. i am BATMAN!')
    elif 'современ' in message.lower():
        update.message.reply_text(anecAPI.modern_joke())
    else:
        update.message.reply_text(f'Я поймал сообщение: {message}')


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

plus_handler = CommandHandler('plus', plus)
minus_handler = CommandHandler('minus', minus)
mult_handler = CommandHandler('mult', mult)
div_handler = CommandHandler('div', div)
echo_handler = CommandHandler('echo', echo)
start_handler = CommandHandler('start', start)
hello_handler = CommandHandler('hello', hello)
bye_handler = CommandHandler('bye', bye)
contact_handler = CommandHandler('contact', send_contact)
joke_handler = MessageHandler(Filters.text, make_jokes)


dispatcher.add_handler(plus_handler)
dispatcher.add_handler(minus_handler)
dispatcher.add_handler(mult_handler)
dispatcher.add_handler(div_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(hello_handler)
dispatcher.add_handler(bye_handler)
dispatcher.add_handler(contact_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(joke_handler)




print('server started')
updater.start_polling()
updater.idle()#ctrl + C
