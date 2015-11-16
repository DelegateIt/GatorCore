FROM ubuntu:14.04
MAINTAINER Austin Middleton

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y\
    python3-pip\
    nodejs\
    npm

#pip is installed but needs to upgraded because the apt repo is behind
RUN pip3 install --upgrade pip

#the upgrade version of pip runs as `pip` NOT `pip3`
RUN pip install\
    boto\
    jsonpickle\
    requests\
    nose

RUN ln -s /usr/bin/nodejs /usr/bin/node

ADD source /var/gator/api
RUN npm install -g aws-sdk socket.io express body-parser socket.io-client

RUN addgroup --gid 4000 gator
RUN useradd --gid 4000 --no-create-home gator

EXPOSE 8060

ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json

USER gator
WORKDIR /var/gator/api/notify
ENV NODE_PATH=/usr/local/lib/node_modules
ENTRYPOINT ["nodejs", "socketio.js"]
