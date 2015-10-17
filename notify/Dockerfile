FROM ubuntu:14.04
MAINTAINER Austin Middleton

RUN apt-get update
RUN apt-get install -y\
    curl\
    build-essential\
    python2.7

RUN curl --silent --location https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install -y nodejs
RUN ln -s /usr/bin/python2.7 /usr/bin/python

ADD source /var/gator/api
RUN npm install -g aws-sdk socket.io express body-parser

RUN addgroup --gid 4000 gator
RUN useradd --gid 4000 --no-create-home gator

EXPOSE 8060

ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json

USER gator
WORKDIR /var/gator/api/notify
ENV NODE_PATH=/usr/lib/node_modules
ENTRYPOINT ["nodejs", "socketio.js"]
