FROM python:3.11

ENV PYTHONWARNINGS="ignore"

RUN apt-get -y update
RUN apt-get install -y libpq-dev

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]
