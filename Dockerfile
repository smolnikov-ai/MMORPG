FROM python:3.13

LABEL authors="smolnikov-ai.dev@ya.ru"

RUN pip install --upgrade pip

WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt

COPY . /code
