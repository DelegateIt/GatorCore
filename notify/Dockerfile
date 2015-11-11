FROM gatbase
MAINTAINER Austin Middleton

RUN apt-get install -y\
    nodejs\
    npm

RUN ln -s /usr/bin/nodejs /usr/bin/node

ADD source /var/gator/api
RUN npm install -g aws-sdk socket.io express body-parser socket.io-client

EXPOSE 8060

ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json

USER gator
WORKDIR /var/gator/api/notify
ENV NODE_PATH=/usr/local/lib/node_modules
ENTRYPOINT ["nodejs", "socketio.js"]
