# Dockerfile, Image, Container
FROM python:3.8

ADD main.py .

RUN pip install telebot

CMD [ "python", "./main.py" ]