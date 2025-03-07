FROM python:3.11-slim

COPY requirements.txt /temp/requirements.txt
COPY requirements.test.txt /temp/requirements.test.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash postgresql-client build-essential libpq-dev && \
    pip install -r /temp/requirements.txt && \
    pip install -r /temp/requirements.test.txt && \
    useradd -m service-user && \
    rm -rf /var/lib/apt/lists/* 
    
COPY src /src
COPY tests /src/tests
COPY pytest.ini /src/pytest.ini
WORKDIR /src

EXPOSE 8000


#CMD alembic upgrade head; python main.py
CMD pwd;ls -AlF;ls -AlF /temp; python main.py
