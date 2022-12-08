#!/bin/env python

import datetime
from bot_files.private import secrets
import telebot
import time
from sqlalchemy.orm import Session
from modules import tea, pidor, nahui, models, vpizdu, zaebal, pinus

bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))

cooldown = {}
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
    nahui.idi_na_huy(msg, bot)


@bot.message_handler(commands=["vpizdu"])
def idi_v_pizdu_wrapper(msg):
    vpizdu.idi_v_pizdu(msg, bot)


@bot.message_handler(commands=["zaebal"])
def zaebal_wrapper(msg) -> None:
    print(cooldown)
    if msg.from_user.username not in cooldown or (datetime.datetime.now() - cooldown[msg.from_user.username]).total_seconds() > 10:
        zaebal.zaebal(msg, bot)
        cooldown[msg.from_user.username] = datetime.datetime.now()
        print((datetime.datetime.now() - cooldown[msg.from_user.username]).total_seconds())
    elif (datetime.datetime.now() - cooldown[msg.from_user.username]).total_seconds() < 10:
        bot.send_message(msg.chat.id, f'Ты заебал, подожди немного!') 

@bot.message_handler(regexp= 'ч(а|я)[ейкаю-я]')
def send_tea(msg):
    bot.send_sticker(msg.chat.id, tea.random_sticker)

@bot.message_handler(commands=['pinus'])
def self_pinus(msg):
    try:
        pinus.personal_pinus(msg, bot)
    except:
        pass
@bot.message_handler(commands=['pinus_fight'])
def pinus_fight(msg):
    try:
        pinus.pinus_fight(msg, bot)
    except:
        pass
bot.polling(none_stop=True, interval=0)