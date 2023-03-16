#!/bin/env python

import datetime
from bot_files.private import secrets, debug_chat
import telebot
import time
from sqlalchemy.orm import Session
from modules import tea, pidor, nahui, models, vpizdu, zaebal, pinus
from modules.logger import logger
import traceback

bot = telebot.TeleBot(secrets.get('BOT_TOKEN'))

cooldown_dict = {}
engine = models.engine
session = Session(engine)

def cooldown(func, cooldown_dict, msg, bot):
    try:
        if msg.from_user.username not in cooldown_dict or (datetime.datetime.now() - cooldown_dict[msg.from_user.username]).total_seconds() > 10:
            func(msg, bot)
            cooldown_dict[msg.from_user.username] = datetime.datetime.now()
        elif (datetime.datetime.now() - cooldown_dict[msg.from_user.username]).total_seconds() < 10:
            bot.send_message(msg.chat.id, f'Ты заебал, подожди немного!') 
            bot.delete_message(msg.chat.id, msg.message_id)
    except Exception as e:
        logger.exception('cooldown func')

@bot.message_handler(commands=["pidor"])
def start(m, res=False):
    try:
        bot.send_message(m.chat.id, f'А может ты пидор?')
    except Exception: 
        logger.exception('pidor func')
        bot.send_message(debug_chat, f'pidor func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=['pidor_reg'])
def start(msg, res=False):
    try:
        pidor.pidor_reg(msg, bot, session)
    except Exception: 
        logger.exception('pidor_reg func')
        bot.send_message(debug_chat, f'pidor_reg func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=['pidor_list'])
def start(msg, res=False):
    try:
        pidor.pidor_list(msg, bot, session)
    except Exception: 
        logger.exception('pidor_list func')
        bot.send_message(debug_chat, f'pidor_list func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    try:
        pidor.find_pidor(msg, bot, session)
    except Exception: 
        logger.exception('find_pidor func')
        bot.send_message(debug_chat, f'find_pidor func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    try:
        pidor.get_pidor_today(msg, bot, session)
    except Exception:
        logger.exception('find_pidor func')
        bot.send_message(debug_chat, f'find_pidor func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=["nah", "nahuy", "nahui", "idinahui", "idinahuy"])
def idi_na_hui_wrapper(msg):
    try:
        cooldown(nahui.idi_na_huy, cooldown_dict, msg, bot)
    except Exception: 
        logger.exception('nah func')
        bot.send_message(debug_chat, f'nah func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=["vpizdu"])
def idi_v_pizdu_wrapper(msg):
    try:
        cooldown(vpizdu.idi_v_pizdu, cooldown_dict, msg, bot)
    except Exception: 
        logger.exception('vpizdu func')
        bot.send_message(debug_chat, f'vpizdu func: {traceback.format_exc()}')
        pass


@bot.message_handler(commands=["zaebal"])
def zaebal_wrapper(msg) -> None:
    try:
        cooldown(zaebal.zaebal, cooldown_dict, msg, bot)
    except Exception: 
        logger.exception('zaebal func')
        bot.send_message(debug_chat, f'vpizdu func: {traceback.format_exc()}')
        pass
       

@bot.message_handler(regexp=r'\bча[йюе]((ку)|(и)|(ей))?\b')
def send_tea(msg):
    try:
        bot.send_sticker(msg.chat.id, tea.random_sticker)
    except Exception: 
        logger.exception('tea func')
        bot.send_message(debug_chat, f'tea func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=['pinus'])
def self_pinus(msg):
    try:
        pinus.personal_pinus(msg, bot)
    except Exception:
        logger.exception('pinus func')
        bot.send_message(debug_chat, f'pinus func: {traceback.format_exc()}')
        pass

@bot.message_handler(commands=['pinus_fight'])
def pinus_fight(msg):
    try:
        pinus.pinus_fight(msg, bot)
    except Exception:
        logger.exception('pinus_fight func')
        bot.send_message(debug_chat, f'pinus_fight func: {traceback.format_exc()}')
        pass


bot.infinity_polling(timeout=10, long_polling_timeout = 5)