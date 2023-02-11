from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
GO = "Вперед" # то, что написано на кнопке
BEGIN, GAME = 1, 2 # 1 шаг разговора

def start(update: Update, context: CallbackContext):
    button = [[GO]]
    keyboard = ReplyKeyboardMarkup(button, resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='Нажми на кнопку')
    update.message.reply_text(
        f"""Ты любишь придумывать сказки? 
        Я очень люблю. Ты знаешь сказку, как посадил дед репку?
        А кто помогал деду репку тянуть? Чтобы начать, нажми на кнопку {GO}!""" , 
        reply_markup=keyboard)
    return BEGIN # переход к следующему шагу

def begin(update: Update, context: CallbackContext):
    heroes = [['дедку'], ['дедка', "репку"]] 
    context.user_data['heroes'] = heroes
    update.message.reply_text('Посадил дедка репку, выросла репка большая-пребольшая. Решил дедка вытянуть репку, тянет-потянет, вытянуть не может. Кого дедка позвал к себе на помощь?', reply_markup = ReplyKeyboardRemove())
    return GAME

def game (update: Update, context: CallbackContext):
    text = update.message.text
    text = morph.parse(text)[0]
    if text.tag.animacy == 'anim':
        nomn = text.inflect({'nomn'}).word
        accs = text.inflect({'accs'}).word
        heroes = context.user_data["heroes"]
        heroes[0].insert(0, nomn)
        heroes.insert(0, accs)
        update.message.reply_text(f'{nomn}, {accs}')
        answer = (f'Я {nomn}, я помогу вам')
        
    else:
        update.message.reply_text(f'Мы долго пытались уговорить {text.normal_form} помочь нам, но он нас просто проигнорировал')


def end(update: Update, context: CallbackContext):
    update.message.reply_text('Значит, ты выбрал конец')
    return ConversationHandler.END