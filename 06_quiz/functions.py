from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import csv
import random

GO = 'Вперёд'
QUESTION_COUNT = 10
GAME, FINISH = 1, 2
RIGHT_ANSWER_COUNT = 0

def read_csv():
    with open('06_quiz\questions.csv', 'r', encoding = 'utf-8') as file:
        quest = list(csv.reader(file, delimiter = '|'))
        return quest
    

def write_csv():
    with open('06_quiz\questions.csv', 'a', encoding = 'utf-8') as file:
        black = csv.writer(file, delimiter = '|', lineterminator = '\n')
        black.writerow(['В какой стране проходили летние Олимпийские игры 2016 года?','Китай','Ирландия','Бразилия','Италия'])


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up,
        resize_keyboard = True,
        one_time_keyboard = True,
        input_field_placeholder = f'Нажми на кнопку "{GO}", поиграем!'
    )
    update.message.reply_text('Добро пожаловать в викторину, вам будет показан один вопрос и 4 варианта ответа на него, среди которых есть только один правильный, ваша задача выбрать его')
    update.message.reply_text(f'Если хотите начать игру, то нажмите кнопку{GO}', reply_markup = keyboard)
    questions = read_csv()
    random.shuffle(questions)
    questions = questions[QUESTION_COUNT:]
    context.user_data['вопросы'] = questions
    return GAME
    

def game(update: Update, context: CallbackContext):
    if QUESTION_COUNT <= 0:
        update.message.reply_text(f'Вы ответили на {RIGHT_ANSWER_COUNT} вопросов')
        if RIGHT_ANSWER_COUNT == 0:
            update.message.reply_text('Вам надо тренироваться')
        elif RIGHT_ANSWER_COUNT <= 4 & RIGHT_ANSWER_COUNT != 0:
            update.message.reply_text('Вы можете лучше')
        elif RIGHT_ANSWER_COUNT >= 4 & RIGHT_ANSWER_COUNT <= 6:
            update.message.reply_text('Неплохо, почти половина ответов были правильными')
        elif RIGHT_ANSWER_COUNT >= 6 & RIGHT_ANSWER_COUNT <= 9:
            update.message.reply_text('Очень хорошо, вы были недалеки от идеала')
        elif RIGHT_ANSWER_COUNT == 10:
            update.message.reply_text('Идеально!')
            return ConversationHandler.END
    questions = context.user_data['вопросы']
    answer = questions.pop()
    question_text = answer.pop(0)
    right_answer = answer[0]
    random.shuffle(answer)
    mark_up = [answer[2:], answer[:2]]
    keyboard = ReplyKeyboardMarkup(
        keyboard = mark_up,
        resize_keyboard = True
        )
    update.message.reply_text(question_text, reply_markup = keyboard)
    QUESTION_COUNT -= 1
    if update.message.text == right_answer:
        RIGHT_ANSWER_COUNT += 1
    
    if QUESTION_COUNT == 0:
        update.message.reply_text(f'Вы ответили на {RIGHT_ANSWER_COUNT} вопросов')
        if RIGHT_ANSWER_COUNT == 0:
            update.message.reply_text('Вам надо тренироваться')
        elif RIGHT_ANSWER_COUNT <= 4 & RIGHT_ANSWER_COUNT != 0:
            update.message.reply_text('Вы можете лучше')
        elif RIGHT_ANSWER_COUNT >= 4 & RIGHT_ANSWER_COUNT <= 6:
            update.message.reply_text('Неплохо, почти половина ответов были правильными')
        elif RIGHT_ANSWER_COUNT >= 6 & RIGHT_ANSWER_COUNT <= 9:
            update.message.reply_text('Очень хорошо, вы были недалеки от идеала')
        elif RIGHT_ANSWER_COUNT == 10:
            update.message.reply_text('Идеально!')
            return ConversationHandler.END
    
    
def end(update: Update, context: CallbackContext):
    name = context.user_data['имя']
    update.message.reply_text(f"Это конец, {name}")
    return ConversationHandler.END