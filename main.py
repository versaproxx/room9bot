#!/bin/env python

import datetime
from bot_files.private import secrets
import telebot
import time
from sqlalchemy.orm import Session
from modules import tea, pidor, nahui, models, vpizdu, zaebal, pinus

bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))

cooldown_dict = {}
engine = models.engine
session = Session(engine)

def cooldown(func, cooldown_dict, msg, bot):
    if msg.from_user.username not in cooldown_dict or (datetime.datetime.now() - cooldown_dict[msg.from_user.username]).total_seconds() > 10:
        func(msg, bot)
        cooldown_dict[msg.from_user.username] = datetime.datetime.now()
    elif (datetime.datetime.now() - cooldown_dict[msg.from_user.username]).total_seconds() < 10:
        bot.send_message(msg.chat.id, f'Ты заебал, подожди немного!') 
        bot.delete_message(msg.chat.id, msg.message_id)

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
    cooldown(nahui.idi_na_huy, cooldown_dict, msg, bot)

@bot.message_handler(commands=["vpizdu"])
def idi_v_pizdu_wrapper(msg):
    cooldown(vpizdu.idi_v_pizdu, cooldown_dict, msg, bot)

@bot.message_handler(commands=["zaebal"])
def zaebal_wrapper(msg) -> None:
    cooldown(zaebal.zaebal, cooldown_dict, msg, bot)
       

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