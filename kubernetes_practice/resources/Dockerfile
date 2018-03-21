ARG VERSION=xenial
FROM registry.docker-cn.com/library/ubuntu:$VERSION
RUN apt update
RUN apt install -y python3
RUN mkdir /scripts
COPY server.py /scripts
RUN apt install -y git
RUN apt install -y vim
RUN apt install -y curl
RUN /usr/local/bin/python3 /scripts/server.py > /dev/null 2>&1 &
RUN /usr/bin/curl localhost:8088
