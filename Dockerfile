FROM ubuntu:latest

RUN apt-get update && apt install python3-dev libpq-dev python3-distutils -y
RUN apt-get install curl -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py

COPY . /hasker
WORKDIR /hasker
RUN pip3 install -r requirements/prod.txt
EXPOSE 8000