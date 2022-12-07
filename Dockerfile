FROM python:3

ENV BOT_HOME /opt/9bot

RUN mkdir -p {BOT_HOME}
WORKDIR ${BOT_HOME}

COPY modules ${BOT_HOME}/modules
COPY ["main.py", "requirements.txt", "${BOT_HOME}/"]

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
