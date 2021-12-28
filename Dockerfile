FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y iputils-ping

# RUN curl -sL https://get.kubemq.io/install | sh

COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

WORKDIR /app
COPY ./src ./src
COPY ./scripts/start-faust-app ./
COPY ./scripts/faust-produce ./
