FROM python:3.9

RUN pip install discord.py aiocron

COPY main.py .

RUN mkdir data

ENTRYPOINT python3 main.py
