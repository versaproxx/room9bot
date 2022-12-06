from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, Date, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///pidors.db', echo=True, future=True, connect_args={'check_same_thread': False})
Base = declarative_base()


class Pidors(Base):
    __tablename__ = 'pidors'

    pidor_id = Column(Integer, primary_key=True)
    name = Column(String)
    pidor_times = Column(Integer)
    pidor_dates = relationship('PidorDates', backref=backref('pidors'))
    UniqueConstraint('name', name='uix_1')
        
class PidorDates(Base):
    __tablename__ = 'pidor_dates'

    date_id = Column(Integer, primary_key=True)
    pidor_id = Column(Integer, ForeignKey('pidors.pidor_id'), nullable=False)
    pidor_date = Column(Date)

Base.metadata.create_all(engine)