FROM delegateit/gatbase
MAINTAINER Austin Middleton

RUN apt-get install -y\
    nodejs\
    npm

RUN ln -s /usr/bin/nodejs /usr/bin/node
ENV NODE_PATH=/usr/local/lib/node_modules
RUN npm install -g aws-sdk socket.io express body-parser socket.io-client

ADD source /var/gator/api
WORKDIR /var/gator/api/notify
USER gator
EXPOSE 8060
ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json
ENTRYPOINT ["nodejs", "socketio.js"]
