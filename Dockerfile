FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y sudo wget vim curl unzip less expect && \
    apt-get install -y python3.9 python3-pip python3-dev

COPY requirement.txt /tmp

RUN cd /tmp && pip install -r requirement.txt

WORKDIR /app