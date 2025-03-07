FROM python:3.11-slim

COPY requirements.txt /temp/requirements.txt
COPY src /src
WORKDIR /src

EXPOSE 8000

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash postgresql-client build-essential libpq-dev && \
    pip install -r /temp/requirements.txt && \
    useradd -m service-user && \
    rm -rf /var/lib/apt/lists/* 

CMD alembic upgrade head; python main.py
#CMD pwd;ls -AlF;ls -AlF /temp; python main.py
