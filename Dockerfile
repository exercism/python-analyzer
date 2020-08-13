FROM python:3.8-slim

RUN mkdir /opt/analyzer
COPY . /opt/analyzer
WORKDIR /opt/analyzer

RUN pip install -r requirements.txt