import random
import csv
import datetime
import time
from sqlalchemy import select, func
from modules.models import Pidors, PidorDates

def pidorList(session):
    pidor_list = []
    pidor_select = select(Pidors.name)
    for pidor in session.scalars(pidor_select):
        pidor_list.append(pidor)
    return pidor_list


def get_pidor(session):
    pidor_of_the_day = random.choice(pidorList(session))
    new_date = PidorDates(pidor_date=datetime.datetime.today(), pidor_id=session.query(Pidors.pidor_id).filter(Pidors.name == pidor_of_the_day))
    session.add(new_date)
    session.commit()
    return pidor_of_the_day


def get_date(session):
    last_date = session.query(func.max(PidorDates.pidor_date)).one()
    print(last_date)
    return last_date[0]


def pidor_reg(msg, bot, session):
    try:
        session.query(Pidors.name).filter(Pidors.name==msg.from_user.username).one()
        bot.send_message(msg.chat.id, 'Эй! Ты уже в игре!')
    except:
        session.add(Pidors(name=msg.from_user.username, pidor_times=0))
        session.commit()
        bot.send_message(msg.chat.id, f'Вы добавлены в игру, {msg.from_user.first_name} (@{msg.from_user.username})')

def get_pidor_today(msg, bot, session):
    pidor_today = session.query(Pidors.name).join(PidorDates).filter(PidorDates.pidor_date == session.query(func.max(PidorDates.pidor_date))).one()
    bot.send_message(msg.chat.id, f'Пидор дня: {pidor_today[0]}')

def pidor_list(msg, bot, session):
    pidor_list = pidorList(session)
    stringa = '\n'.join(pidor_list)
    bot.send_message(msg.chat.id, stringa)

def find_pidor(msg, bot, session):
    phraseList = [f'Кто же этот пидор, что спиздил у меня головку на {random.randint(8, 32)}', 'Список не большой',
              'Сейчас посмотрим']
    if get_date(session) == None:
        last_date = datetime.date(1970, 1, 1)
    else:
        last_date = get_date(session)
    if last_date >= datetime.datetime.today().date():
        get_pidor_today(msg, bot, session)
    elif last_date < datetime.datetime.today().date():
        pidor = get_pidor(session)
        for phrase in phraseList:
            bot.send_message(msg.chat.id, phrase)
            time.sleep(3)
        bot.send_message(msg.chat.id, f'Новый пидор дня сегодня: @{pidor}')