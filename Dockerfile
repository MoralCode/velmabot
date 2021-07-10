FROM python:3.9-slim-buster

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY main.py .
COPY lines.txt .

RUN mkdir data

ENTRYPOINT pipenv run python3 main.py
