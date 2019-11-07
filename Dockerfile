FROM python:3

COPY . /bot
WORKDIR /bot
RUN pip install -r requirements.txt
ENTRYPOINT python /bot/bot.py
