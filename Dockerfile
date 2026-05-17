FROM python:3.13-alpine3.23

COPY requirements.txt /requirements.txt

RUN apk update && apk upgrade \
 && apk --no-cache add bash \
 && apk cache clean

RUN --mount=type=cache,target=/root/.cache/pip \
 PYTHONDONTWRITEBYTECODE=1 \
 pip install --no-compile  --no-cache \
 -r /requirements.txt

COPY . /opt/analyzer

WORKDIR /opt/analyzer

ENTRYPOINT ["sh", "/opt/analyzer/bin/run.sh"]
