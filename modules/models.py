from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Table, create_engine, Date, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bot_files/pidors.db', echo=True, future=True, connect_args={'check_same_thread': False})
Base = declarative_base()

class Pidors(Base):
    __tablename__ = 'pidors'

    pidor_id = Column(Integer, primary_key=True)
    name = Column(String)
    pidor_times = Column(Integer, default=0)
    pidor_dates = relationship('PidorDates', backref=backref('pidors'))
    chat_id = Column(Integer)
    UniqueConstraint('name', 'chat_id', name='uix_1')


class PidorDates(Base):
    __tablename__ = 'pidor_dates'

    date_id = Column(Integer, primary_key=True)
    pidor_id = Column(Integer, ForeignKey('pidors.pidor_id'), nullable=False)
    pidor_date = Column(Date)
    chat_id = Column(Integer, nullable=False)

Base.metadata.create_all(engine)