ARG VERSION=xenial
FROM registry.docker-cn.com/library/ubuntu:$VERSION
RUN apt update
RUN apt install -y python3
#RUN apt install -y git
#RUN apt install -y vim
RUN apt install -y curl
#RUN apt install -y screen
COPY server.py /root/
COPY start-server.sh /root/
RUN chmod 755 /root/start-server.sh
#ENTRYPOINT ["/bin/sh", "/root/start-server.sh"]


#test1:
# > docker run -i -t -d --name server-test -p 127.0.0.1:8088:8088 server:test1
# > docker exec server-test /root/start-server.sh
# > docker exec server-test curl localhost:8088
# > "hello"
# > curl localhost:8088
# > curl: (52) Empty reply from server


#test2
# > docker run -i -t -d --name server-test -P server:test1 /root/start-server.sh
# > docker ps
# The container server-test is not start


