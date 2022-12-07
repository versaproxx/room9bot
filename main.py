#!/bin/env python

from bot_files.private import secrets
import telebot
from sqlalchemy.orm import Session
from modules import tea, pidor, nahui, models, vpizdu
from os import system

bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))

engine = models.engine
session = Session(engine)

@bot.message_handler(commands=["pidor"])
def start(m, res=False):
    try:
        bot.send_message(m.chat.id, f'А может ты пидор?')
    except:
        pass

@bot.message_handler(commands=['pidor_reg'])
def start(msg, res=False):
    try:
        pidor.pidor_reg(msg, bot, session)
    except:
        pass

@bot.message_handler(commands=['pidor_list'])
def start(msg, res=False):
    try:
        pidor.pidor_list(msg, bot, session)
    except:
        pass

@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    try:
        pidor.find_pidor(msg, bot, session)
    except:
        pass

@bot.message_handler(commands=["nah", "nahuy", "nahui", "idinahui", "idinahuy"])
def idi_na_hui_wrapper(msg):
    try:
        nahui.idi_na_huy(msg, bot)
    except:
        pass

@bot.message_handler(commands=["vpizdu"])
def idi_v_pizdu_wrapper(msg):
    try:
        vpizdu.idi_v_pizdu(msg, bot)
    except:
        pass

@bot.message_handler(regexp= 'ч(а|я)[ейкаю-я]')
def send_tea(msg):
    bot.send_sticker(msg.chat.id, tea.random_sticker)

@bot.message_handler(commands=["git_update"])
def version_update(msg):
    if msg.from_user.id in [207307299, 5217820769, 493821534]:
        try:
            bot.send_message(msg.chat.id, f'Start update.')
            os.system('sh new_build.sh')
        except:
            pass
    else:
        bot.send_message(msg.chat.id, f'Not allowed')

bot.polling(none_stop=True, interval=0)
