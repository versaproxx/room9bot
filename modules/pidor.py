import random
import datetime
import time
from sqlalchemy import select, func, Column, Integer, BigInteger, String, and_
from sqlalchemy.future import engine
from sqlalchemy.sql.operators import exists

from modules.models import Pidors, PidorDates, Base

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
    session.query(Pidors).filter(Pidors.name == pidor_of_the_day).update({'pidor_times': session.query(Pidors.pidor_times).filter(Pidors.name == pidor_of_the_day).one()[0] + 1})
    session.commit()
    return pidor_of_the_day


def get_date(session):
    last_date = session.query(func.max(PidorDates.pidor_date)).one()
    print(last_date)
    return last_date[0]


# def pidor_reg(msg, bot, session):
#     username = msg.from_user.username
#     if username:
#         if session.query(Pidors.name).filter(Pidors.name==username).scalar():
#             bot.send_message(msg.chat.id, 'Эй! Ты уже в игре!')
#         else:
#             session.add(Pidors(name=username, pidor_times=0))
#             session.commit()
#             bot.send_message(msg.chat.id, f'Вы добавлены в игру, {msg.from_user.first_name} (@{username})')
#     else:
#         bot.send_message(msg.chat.id, 'Ты, Rising Sun, и так пидор по умолчанию')
class ChatPlayers(Base):
    __tablename__ = 'chat_players'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    username = Column(String(50))
    pidor_times = Column(Integer, default=0)

    def __init__(self, chat_id, username):
        self.chat_id = chat_id
        self.username = username
def pidor_reg(msg, bot, session):
    try:
        chat_id = msg.chat.id
        username = msg.from_user.username

        if not session.query(exists().where(and_(ChatPlayers.chat_id == chat_id))).scalar():
            Base.metadata.tables['chat_players'].create(bind=engine, checkfirst=True)

        player = session.query(ChatPlayers).filter(and_(ChatPlayers.chat_id == chat_id, ChatPlayers.username == username)).first()
        if player:
            bot.send_message(msg.chat.id, 'Эй! Ты уже в игре!')
        else:
            if msg.from_user.username is not None:
                new_player = ChatPlayers(chat_id, msg.from_user.username)
                session.add(new_player)
                session.commit()
                bot.send_message(msg.chat.id, f'Вы добавлены в игру, {msg.from_user.first_name} (@{msg.from_user.username})')
            else:
                bot.send_message(msg.chat.id, f'Ты, Rising Sun, и так пидор по умолчанию')
    except Exception as e:
        bot.send_message(msg.chat.id, f'Ошибка: {str(e)}')
def get_pidor_today(msg, bot, session):
    pidor_today = session.query(Pidors.name).join(PidorDates).order_by(PidorDates.pidor_date.desc()).first()
    if pidor_today:
        bot.send_message(msg.chat.id, f'Пидор дня: {pidor_today[0]}')
    else:
        bot.send_message(msg.chat.id, 'Пока никто не стал пидором дня')

def pidor_list(msg, bot, session):
    pidor_list_text = ''
    pidor_list = pidorList(session)
    pidor_dict = {}
    for pidor in pidor_list:
        pidor_count = session.query(Pidors.pidor_times).filter(Pidors.name==pidor).one()
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

# def find_pidor(msg, bot, session):
#     last_date = get_date(session) or datetime.date(1970, 1, 1)
#     if last_date >= datetime.date.today():
#         get_pidor_today(msg, bot, session)
#     else:
#         pidor = get_pidor(session)
#         for phrase in PHRASE_LIST:
#             bot.send_message(msg.chat.id, phrase)
#             time.sleep(3)
#         bot.send_message(msg.chat.id, f'Новый пидор дня сегодня: @{pidor}')

def find_pidor(msg, bot, session):
    try:
        chat_id = msg.chat.id

        if not session.query(exists().where(and_(ChatPlayers.chat_id == chat_id))).scalar():
            bot.send_message(msg.chat.id,
                             'В этом чате еще никто не зарегистрирован. Используйте команду /pidor_reg чтобы зарегистрироваться.')
            return

        # Получаем всех игроков текущего чата
        chat_players = session.query(ChatPlayers).filter(ChatPlayers.chat_id == chat_id).all()

        today = datetime.today().strftime('%Y-%m-%d')
        pidor_today = session.query(ChatPlayers.username).join(PidorDates).filter(
            and_(PidorDates.pidor_date == today, ChatPlayers.chat_id == chat_id,
                 ChatPlayers.id == PidorDates.player_id)).all()
        available_players = [p for p in chat_players if p.username not in [pt[0] for pt in pidor_today]]
        if not available_players:
            bot.send_message(msg.chat.id, 'Все уже были пидорами сегодня. Приходите завтра.')
            return
        pidor = random.choice(available_players)

        new_pidor_date = PidorDates(player_id=pidor.id, pidor_date=today)
        session.add(new_pidor_date)
        pidor.pidor_times += 1
        session.commit()

        bot.send_message(msg.chat.id, f'Пидор дня: {pidor.username}')
    except Exception as e:
        bot.send_message(msg.chat.id, f'Ошибка: {str(e)}')