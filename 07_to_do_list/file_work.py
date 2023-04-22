from telegram.ext import CallbackContext
from telegram import Update
from config import *
from constants import *
from stickers import *
import csv
import os


def init(update: Update, context: CallbackContext):
    username = update.effective_user.username
    filename = f'userdata_bank/{username}.csv'
    context.user_data['file'] = filename
    if not os.path.exists('userdata_bank'):
        os.mkdir('userdata_bank')
    if not os.path.exists(filename):
        open(filename, 'w', encoding='utf-8')
    

def read_csv():
    with open('06_quiz\questions.csv', 'r', encoding = 'utf-8') as file:
        quest = list(csv.reader(file, delimiter = '|'))
    

def write_csv():
    with open('06_quiz\questions.csv', 'a', encoding = 'utf-8') as file:
        black = csv.writer(file, delimiter = '|', lineterminator = '\n')
        black.writerow(['В какой стране проходили летние Олимпийские игры 2016 года?','Китай','Ирландия','Бразилия','Италия'])
