#!/bin/env python

from bot_files.private import secrets
import telebot
from sqlalchemy.orm import Session
from modules import tea, pidor, nahui, models, vpizdu
import random


bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))

engine = models.engine
session = Session(engine)

@bot.message_handler(commands=["pidor"])
def start(m, res=False):
    try:
        bot.send_message(m.chat.id, f'А может ты пидор?')
    except Exception as e: 
        print(e)
        pass

@bot.message_handler(commands=['pidor_reg'])
def start(msg, res=False):
    try:
        pidor.pidor_reg(msg, bot, session)
    except Exception as e: 
        print(e)
        pass

@bot.message_handler(commands=['pidor_list'])
def start(msg, res=False):
    try:
        pidor.pidor_list(msg, bot, session)
    except Exception as e: 
        print(e)
        pass

@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    try:
        pidor.find_pidor(msg, bot, session)
    except Exception as e: 
        print(e)
        pass

@bot.message_handler(commands=["nah", "nahuy", "nahui", "idinahui", "idinahuy"])
def idi_na_hui_wrapper(msg):
    try:
        nahui.idi_na_huy(msg, bot)
    except Exception as e: 
        print('externa exc')
        print(e)
        pass

@bot.message_handler(commands=["vpizdu"])
def idi_v_pizdu_wrapper(msg):
    try:
        vpizdu.idi_v_pizdu(msg, bot)
    except Exception as e: 
        print(e)
        pass

@bot.message_handler(regexp= 'ч(а|я)[ейкаю-я]')
def send_tea(msg):
    bot.send_sticker(msg.chat.id, tea.random_sticker)

@bot.message_handler(commands=['pinus'])
def pinus(msg):
    raw_pinus = msg.reply_to_message.from_user.id
    size = 0
    for raw_size in raw_pinus:
        size += int(raw_size)
    bot.send_message(msg.chat.id, f"Твой пинус: {(size / 2) + random.randint(0,9)}")


bot.polling(none_stop=True, interval=0)