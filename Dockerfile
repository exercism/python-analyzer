FROM python:3.7-slim

ENV TOOLING_WEBSERVER_VERSION="0.10.0"
ENV TOOLING_WEBSERVER_URL="https://github.com/exercism/tooling-webserver/releases/download/${TOOLING_WEBSERVER_VERSION}/tooling_webserver"

RUN apt-get update \
 && apt-get install curl -y \
 && curl -L -o /usr/local/bin/tooling_webserver "$TOOLING_WEBSERVER_URL" \
 && chmod +x /usr/local/bin/tooling_webserver \
 && apt-get remove curl -y \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/analyzer
COPY . /opt/analyzer
WORKDIR /opt/analyzer

RUN pip install -r requirements.txt
