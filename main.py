#!/bin/env python

import telebot
import random
import csv
import datetime

bot = telebot.TeleBot('5921046052:AAEPrPhFvrRPPdm5Rri0RaMYa_Hak_KQRvw')

pidor_list = []
phraseList = [f'Кто же этот пидор, что спиздил у меня головку на {random.randint(8,32)}', 'Список не большой', 'Сейчас посмотрим']

def pidorList():
    with open(r'/Users/badm/Documents/python_learning /users.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            pidor_list.append(row[0])
        f.close()
    return pidor_list
pidorList()

def getPidor():
    pidor_of_the_day = random.choice(pidor_list)
    with open (r'/Users/badm/Documents/python_learning /ristrinctDate.csv', mode='a', newline='\n', encoding='utf-8') as dateFile:
        dateWriter = csv.writer(dateFile, delimiter=',', quotechar='"')
        dateWriter.writerow([datetime.datetime.today().strftime('%Y-%m-%d'), pidor_of_the_day])
        dateFile.close()
    return pidor_of_the_day


def getDate():
    with open(r'/Users/badm/Documents/python_learning /ristrinctDate.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            last_played_date = row[0]
            print(row[0])
    f.close()
    return last_played_date

getDate()
def registerPidor(msg):
        with open('/Users/badm/Documents/python_learning /users.csv', mode='a', newline='\n', encoding='utf-8') as users_file:
            pidor_writer = csv.writer(users_file, delimiter=',', quotechar='"')
            pidor_writer.writerow([msg.from_user.username, 0])
            users_file.close()
        pidor_list.append(msg.from_user.username)
        bot.send_message(msg.chat.id, f'Вы добавлены в игру, {msg.from_user.first_name} (@{msg.from_user.username})')

def getPidorToday(msg):
        with open(r'/Users/badm/Documents/python_learning /ristrinctDate.csv') as f:
            temp_pidor_list = []
            reader = csv.reader(f)
            for row in reader:
                temp_pidor_list.append(row[1])
            f.close()
        bot.send_message(msg.chat.id, f'Пидор дня: @{temp_pidor_list[-1]}')


@bot.message_handler(commands=["pidor"])
def start(m, res=False):
    bot.send_message(m.chat.id, f'А может ты  пидор ?')

@bot.message_handler(commands=['pidor_reg'])
def start(msg, res=False):
    pidorList()
    if msg.from_user.username in pidor_list:
                 bot.send_message(msg.chat.id, 'Эй! Ты уже в игре!')
    else:
        registerPidor(msg)
        
            
@bot.message_handler(commands=['pidor_list'])
def start(msg, res=False):
    stringa = ','.join(pidor_list)
    bot.send_message(msg.chat.id, stringa)

@bot.message_handler(commands=['find_pidor'])
def start(msg, res=False):
    if datetime.datetime.strptime(getDate(),'%Y-%m-%d').date() >= datetime.datetime.today().date():
        getPidorToday(msg)
    elif datetime.datetime.strptime(getDate(),'%Y-%m-%d').date() < datetime.datetime.today().date():
        for phrase in phraseList:
            bot.send_message(msg.chat.id, phrase)
        bot.send_message(msg.chat.id, f'Новый пидор дня сегодня: @{getPidor()}')
        


bot.polling(none_stop=True, interval=0) 