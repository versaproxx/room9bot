#!/bin/env python

from private import secrets
import telebot

from pidor import pidor_reg, pidor_list, find_pidor
from nahui import idi_na_huy

bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))


@bot.message_handler(commands=["pidor"])
def start(m, res=False):
    bot.send_message(m.chat.id, f'А может ты пидор?')


@bot.message_handler(commands=['pidor_reg'])
def start(msg, res=False):
    pidor_reg(msg, bot)


@bot.message_handler(commands=['pidor_list'])
def start(msg, res=False):
    pidor_list(msg, bot)


@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    find_pidor(msg, bot)


@bot.message_handler(commands=["nah", "nahuy", "nahui", "idinahui", "idinahuy"])
def idi_na_hui_wrapper(msg, bot):
    idi_na_huy(msg,bot)

bot.polling(none_stop=True, interval=0)
