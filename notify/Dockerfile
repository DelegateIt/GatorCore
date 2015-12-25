FROM delegateit/gatbase
MAINTAINER Austin Middleton

ADD source /var/gator/api
WORKDIR /var/gator/api/notify
USER gator
EXPOSE 8060
ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json
ENTRYPOINT ["nodejs", "socketio.js"]
