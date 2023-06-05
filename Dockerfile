FROM python:3.10-alpine

RUN mkdir /app
WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk add postgresql-client build-base postgresql-dev
RUN pip install --upgrade pip

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/src .

ENV PYTHONPATH=/app
