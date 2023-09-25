import random
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


def get_pidor(msg,session):
    chat_id = msg.chat.id
    pidor_of_the_day = random.choice(pidorList(session))
    new_date = PidorDates(pidor_date=datetime.datetime.today(), pidor_id=session.query(Pidors.pidor_id).filter(Pidors.name == pidor_of_the_day, Pidors.chat_id==chat_id), chat_id = chat_id)
    session.add(new_date)
    session.commit()
    session.query(Pidors).filter(Pidors.name == pidor_of_the_day,Pidors.chat_id==chat_id).update({'pidor_times': session.query(Pidors.pidor_times).filter(Pidors.name == pidor_of_the_day,Pidors.chat_id==chat_id).one()[0] + 1})
    session.commit()
    return pidor_of_the_day


def get_date(session):
    last_date = session.query(func.max(PidorDates.pidor_date)).one()
    print(last_date)
    return last_date[0]


def pidor_reg(msg, bot, session):
    username = msg.from_user.username
    chat_id = msg.chat.id
    if username:
        if session.query(Pidors.name).filter(Pidors.name==username,Pidors.chat_id==chat_id).scalar():
            bot.send_message(msg.chat.id, 'Эй! Ты уже в игре!')
        else:
            session.add(Pidors(name=username, chat_id=chat_id, pidor_times=0))
            session.commit()
            bot.send_message(msg.chat.id, f'Вы добавлены в игру, {msg.from_user.first_name} (@{username})')
    else:
        bot.send_message(msg.chat.id, 'Ты, Rising Sun, и так пидор по умолчанию')
def get_pidor_today(msg, bot, session):
    chat_id = msg.chat.id
    pidor_today = session.query(Pidors.name).filter(Pidors.chat_id==chat_id).join(PidorDates).order_by(PidorDates.pidor_date.desc()).first()
    if pidor_today:
        bot.send_message(msg.chat.id, f'Пидор дня: {pidor_today[0]}')
    else:
        bot.send_message(msg.chat.id, 'Пока никто не стал пидором дня')

def pidor_list(msg, bot, session):
    chat_id = msg.chat.id
    pidor_list_text = ''
    pidor_list = pidorList(session)
    pidor_dict = {}
    for pidor in pidor_list:
        pidor_count = session.query(Pidors.pidor_times).filter(Pidors.name==pidor,Pidors.chat_id==chat_id).one()
        pidor_dict[pidor] = pidor_count
    sorted_pidors = dict(sorted(pidor_dict.items(), key=lambda item: item[1], reverse=True))
    for pidor in sorted_pidors:
        pidor_list_text = pidor_list_text + pidor + ' - ' + str(sorted_pidors[pidor][0]) + ' раз(а)' + '\n'
    bot.send_message(msg.chat.id, pidor_list_text)

PHRASE_LIST = [f'Кто же этот пидор, что спиздил у меня головку на {random.randint(8, 32)}',
               'Надо было не курить, а учиться... Ну что ж, пойдет тебе пидорский титул!',
               'Правила просты: кто был пидором вчера, тот пидор и сегодня. Так что, сегодня ты везунчик!',
               'Хм, ты не знаешь, кто пидор дня? Давай проверим: если ты это читаешь, значит это ты!',
               'А ты знаешь, что делает пидор, когда его выбирают дня? Ничего не делает, он счастлив!',
               'Наши эксперты изменили формулу выбора пидора дня. И теперь вот что она говорит: пидор - это ты!']

def find_pidor(msg, bot, session):
    last_date = get_date(session) or datetime.date(1970, 1, 1)
    if last_date >= datetime.date.today():
        get_pidor_today(msg, bot, session)
    else:
        pidor = get_pidor(session)
        for phrase in PHRASE_LIST:
            bot.send_message(msg.chat.id, phrase)
            time.sleep(3)
        bot.send_message(msg.chat.id, f'Новый пидор дня сегодня: @{pidor}')