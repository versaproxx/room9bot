#!/bin/env python

from private import secrets
import telebot
from sqlalchemy.orm import Session
from modules import tea, pidor, nahui, models

bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))

engine = models.engine
session = Session(engine)

@bot.message_handler(commands=["pidor"])
def start(m, res=False):
    bot.send_message(m.chat.id, f'А может ты пидор?')


@bot.message_handler(commands=['pidor_reg'])
def start(msg, res=False):
    pidor.pidor_reg(msg, bot, session)


@bot.message_handler(commands=['pidor_list'])
def start(msg, res=False):
    pidor.pidor_list(msg, bot, session)


@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    pidor.find_pidor(msg, bot, session)


@bot.message_handler(commands=["nah", "nahuy", "nahui", "idinahui", "idinahuy"])
def idi_na_hui_wrapper(msg):
    nahui.idi_na_huy(msg, bot)

@bot.message_handler(regexp= 'ч(а|я)[ейкаю-я]')
def send_tea(msg):
    bot.send_sticker(msg.chat.id, tea.random_sticker)

bot.polling(none_stop=True, interval=0)
