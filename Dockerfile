FROM python:3.7-alpine

RUN apk add --no-cache gcc libc-dev unixodbc-dev

RUN mkdir /opt/analyzer
COPY . /opt/analyzer
WORKDIR /opt/analyzer

RUN pip install -r requirements.txt