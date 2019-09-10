FROM python:3.6-alpine

RUN adduser -D appuser

WORKDIR /home/appuser

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY cameraemulator.py config.py boot.sh ./

ENV FLASK_APP cameraemulator.py

RUN chown -R appuser:appuser ./
USER appuser

ENTRYPOINT ["./boot.sh"]
