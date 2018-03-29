#
# Redis Dockerfile
#
# https://github.com/dockerfile/redis
#

# Pull base image.
FROM ubuntu

# Install basic environment
RUN apt update
RUN apt install -y wget
RUN apt install -y gcc
RUN apt install -y make


# Install Redis.
RUN \
  cd /tmp && \
  wget http://download.redis.io/redis-stable.tar.gz && \
  tar xvzf redis-stable.tar.gz && \
  cd redis-stable && \
  cd deps && \
  make hiredis jemalloc linenoise lua && \
  cd .. && \
  make && \
  make install && \
  cp -f src/redis-sentinel /usr/local/bin && \
  mkdir -p /etc/redis && \
  cp -f *.conf /etc/redis

# Install ruby environment and ruby-redis
RUN apt install -y rubygems && \
  gem install redis

# Update the configuration of the redis
RUN sed -i 's/^\(daemonize .*\)$/# \1/' /etc/redis/redis.conf && \
  sed -i 's/^\(dir .*\)$/# \1\ndir \/data/' /etc/redis/redis.conf && \
  sed -i 's/^\(logfile .*\)$/# \1/' /etc/redis/redis.conf && \
  sed -i 's/^# cluster-enabled/cluster-enabled/g' /etc/redis/redis.conf && \
  sed -i 's/^appendonly no/appendonly yes/g' /etc/redis/redis.conf && \
  sed -i 's/^bind 127.0.0.1$/bind 0.0.0.0/g' /etc/redis/redis.conf

# Define mountable directories.
VOLUME ["/data"]

# Define working directory.
WORKDIR /data

