FROM python:3.9

RUN pip install discord.py aiocron beautifulsoup4

COPY main.py .

RUN mkdir data

ENTRYPOINT python3 main.py
