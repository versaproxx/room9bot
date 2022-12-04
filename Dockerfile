FROM python:3

ENV BOT_HOME /opt/9bot

RUN mkdir -p {BOT_HOME}
WORKDIR ${BOT_HOME}

COPY ["main.py", "users.csv", "restrictedDates.csv", "requirements.txt", "private.csv" ,${BOT_HOME}]

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]