FROM python:3.13.5-alpine3.22

COPY requirements.txt /requirements.txt
COPY dev-requirements.txt /dev-requirements.txt

RUN pip install -r /requirements.txt -r /dev-requirements.txt

COPY . /opt/analyzer

WORKDIR /opt/analyzer

ENTRYPOINT ["sh", "/opt/analyzer/bin/run.sh"]
