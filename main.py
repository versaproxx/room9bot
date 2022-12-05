#!/bin/env python

from private import secrets
import telebot
import random
import csv
import datetime
import time
from modules import tea
bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))

pidor_list = []
phraseList = [f'Кто же этот пидор, что спиздил у меня головку на {random.randint(8, 32)}', 'Список не большой',
              'Сейчас посмотрим']


def pidorList():
    with open(r'users.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            pidor_list.append(row[0])
    return pidor_list


pidorList()


def get_pidor():
    pidor_of_the_day = random.choice(pidor_list)
    with open(r'restrictedDates.csv', mode='a', newline='\n', encoding='utf-8') as dateFile:
        date_writer = csv.writer(dateFile, delimiter=',', quotechar='"')
        date_writer.writerow([datetime.datetime.today().strftime('%Y-%m-%d'), pidor_of_the_day])
    return pidor_of_the_day


def get_date():
    last_played_date = ''
    with open(r'restrictedDates.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            last_played_date = row[0]
            print(row[0])
    return last_played_date


get_date()


def register_pidor(msg):
    with open(r'users.csv', mode='a', newline='\n', encoding='utf-8') as users_file:
        pidor_writer = csv.writer(users_file, delimiter=',', quotechar='"')
        pidor_writer.writerow([msg.from_user.username, 0])
    pidor_list.append(msg.from_user.username)
    bot.send_message(msg.chat.id, f'Вы добавлены в игру, {msg.from_user.first_name} (@{msg.from_user.username})')


def get_pidor_today(msg):
    with open(r'restrictedDates.csv') as f:
        temp_pidor_list = []
        reader = csv.reader(f)
        for row in reader:
            temp_pidor_list.append(row[1])
    bot.send_message(msg.chat.id, f'Пидор дня: {temp_pidor_list[-1]}')


@bot.message_handler(commands=["pidor"])
def start(m, res=False):
    bot.send_message(m.chat.id, f'А может ты пидор ?')


@bot.message_handler(commands=['pidor_reg'])
def start(msg, res=False):
    pidorList()
    if msg.from_user.username in pidor_list:
        bot.send_message(msg.chat.id, 'Эй! Ты уже в игре!')
    else:
        register_pidor(msg)


@bot.message_handler(commands=['pidor_list'])
def start(msg, res=False):
    stringa = '\n'.join(pidor_list)
    bot.send_message(msg.chat.id, stringa)


@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    if datetime.datetime.strptime(get_date(), '%Y-%m-%d').date() >= datetime.datetime.today().date():
        get_pidor_today(msg)
    elif datetime.datetime.strptime(get_date(), '%Y-%m-%d').date() < datetime.datetime.today().date():
        for phrase in phraseList:
            bot.send_message(msg.chat.id, phrase)
            time.sleep(3)
        bot.send_message(msg.chat.id, f'Новый пидор дня сегодня: @{get_pidor()}')


message_template = "Иди на хуй, {}"


@bot.message_handler(commands=["nah", "nahuy", "nahui", "idinahui", "idinahuy"])
def idi_na_huy(msg):
    deleting_message = msg.message_id
    if '@' in str(msg.text):
        name = str(msg.text).split('@')[1]
        bot.reply_to(msg.reply_to_message.from_user.id, f'Иди на хуй, @{name}')
    else:
        try:
            name = msg.reply_to_message.from_user.username
            bot.send_message(msg.chat.id, f'Иди на хуй, @{name}',  reply_to_message_id=msg.reply_to_message.message_id)
        except:
            bot.send_message(msg.chat.id, f'Ты, засранец вонючий, мать твою, а? Ну, иди сюда, попробуй меня трахнуть – я тебя сам трахну, ублюдок, онанист чертов, будь ты проклят! Иди, идиот, трахать тебя и всю твою семью! Говно собачье, жлоб вонючий, дерьмо, сука, падла! Иди сюда, мерзавец, негодяй, гад! Иди сюда, ты, говно, жопа!') 
        

    bot.delete_message(msg, deleting_message)

bot.message_handler(regexp= 'ча[ю-я]')
def send_tea(msg):
    bot.send_sticker(msg.chat.id, tea.random_sticker)

bot.polling(none_stop=True, interval=0)
