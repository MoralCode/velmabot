FROM python:3.9

COPY main.py .

RUN pip install discord.py aiocron beautifulsoup4

ENTRYPOINT python3 main.py
