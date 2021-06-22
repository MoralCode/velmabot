FROM python:3.9-slim-buster

RUN pip install discord.py aiocron timeago

COPY main.py .

RUN mkdir data

ENTRYPOINT python3 main.py
