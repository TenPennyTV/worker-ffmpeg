FROM python:3.7.2-slim-stretch

MAINTAINER Jimmy Wahlberg "jimmy@tenpenny.tv"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update
RUN yes | apt-get install ffmpeg

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "run.py" ]
