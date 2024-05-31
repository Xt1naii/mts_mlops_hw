FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install make

EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt \
        --no-cache-dir

COPY . /app/

CMD make run_app_docker
