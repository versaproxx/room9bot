import random
import csv
import datetime
import time


def pidorList(pidor_list):
    with open(r'users.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            pidor_list.append(row[0])
    return pidor_list


def get_pidor(pidor_list):
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


def register_pidor(msg, bot, pidor_list):
    with open(r'users.csv', mode='a', newline='\n', encoding='utf-8') as users_file:
        pidor_writer = csv.writer(users_file, delimiter=',', quotechar='"')
        pidor_writer.writerow([msg.from_user.username, 0])
    pidor_list.append(msg.from_user.username)
    bot.send_message(msg.chat.id, f'Вы добавлены в игру, {msg.from_user.first_name} (@{msg.from_user.username})')


def get_pidor_today(msg,bot):
    with open(r'restrictedDates.csv') as f:
        temp_pidor_list = []
        reader = csv.reader(f)
        for row in reader:
            temp_pidor_list.append(row[1])
    bot.send_message(msg.chat.id, f'Пидор дня: {temp_pidor_list[-1]}')

def pidor_reg(msg,bot):
    pidor_list = []
    pidorList(pidor_list)
    if msg.from_user.username in pidor_list:
        bot.send_message(msg.chat.id, 'Эй! Ты уже в игре!')
    else:
        register_pidor(msg, bot, pidor_list)

def pidor_list(msg, bot):
    pidor_list = []
    pidorList(pidor_list)
    stringa = '\n'.join(pidor_list)
    bot.send_message(msg.chat.id, stringa)

def find_pidor(msg, bot):
    get_date()
    pidor_list = []
    pidorList(pidor_list)
    phraseList = [f'Кто же этот пидор, что спиздил у меня головку на {random.randint(8, 32)}', 'Список не большой',
              'Сейчас посмотрим']
    pidor = get_pidor(pidor_list)
    if datetime.datetime.strptime(get_date(), '%Y-%m-%d').date() >= datetime.datetime.today().date():
        get_pidor_today(msg, bot)
    elif datetime.datetime.strptime(get_date(), '%Y-%m-%d').date() < datetime.datetime.today().date():
        for phrase in phraseList:
            bot.send_message(msg.chat.id, phrase)
            time.sleep(3)
        bot.send_message(msg.chat.id, f'Новый пидор дня сегодня: @{pidor}')