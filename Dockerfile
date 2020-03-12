FROM ubuntu:18.04
RUN apt-get update && apt-get install -y software-properties-common curl libpq-dev build-essential
RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt-get update \
  && apt-get install -y python3.7-dev python3.7-distutils

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.7 get-pip.py

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN mkdir /code/api
RUN mkdir /code/weather
COPY requirements.txt /code/
RUN pip3.7 install -r requirements.txt

COPY api/* /code/api/
COPY setup.py /code/

RUN pip3.7 install -e /code/.

RUN mkdir /gunicorn
COPY gunicorn/* /gunicorn/

RUN mkdir /code/uploads
