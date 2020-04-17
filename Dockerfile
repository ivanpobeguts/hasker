FROM ubuntu:latest

RUN apt-get update && apt install python3-dev libpq-dev python3-distutils -y
RUN apt-get install curl -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py

COPY ./requirements.txt /hasker/requirements.txt
WORKDIR /hasker
RUN pip3 install -r requirements.txt