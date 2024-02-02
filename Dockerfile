FROM python:3.11
RUN apt-get update
RUN apt-get install libpq-dev --assume-yes

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]
