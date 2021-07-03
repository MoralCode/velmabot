FROM python:3.9-slim-buster

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY main.py .

RUN mkdir data

ENTRYPOINT python3 main.py
