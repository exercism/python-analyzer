FROM python:3.10.6-slim

RUN apt-get update \
 && apt-get install curl -y \
 && apt-get remove curl -y \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/analyzer
COPY . /opt/analyzer
WORKDIR /opt/analyzer

RUN pip install -r requirements.txt -r dev-requirements.txt
ENTRYPOINT ["/opt/analyzer/bin/run.sh"]
