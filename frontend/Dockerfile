#  Created by Marcello Monachesi at 9/6/19, 5:30 PM

FROM python:3.6-alpine

RUN adduser -D appuser

WORKDIR /home/appuser


RUN python -m venv venv

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN venv/bin/pip install psycopg2

COPY requirements.txt requirements.txt
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY displayserverfrontend.py config.py boot.sh ./

ENV FLASK_APP displayserverfrontend.py

RUN chown -R appuser:appuser ./
USER appuser

ENTRYPOINT ["./boot.sh"]

