ARG VERSION=xenial
FROM ubuntu:$VERSION
RUN apt update
RUN apt -y install python3
RUN mkdir /scripts
COPY server.py /scripts
