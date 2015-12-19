FROM delegateit/gatbase
MAINTAINER Austin Middleton

RUN pip install\
    Flask\
    eventlet\
    gunicorn\
    stripe\
    twilio

ADD source /var/gator/api
WORKDIR /var/gator/api
USER gator
EXPOSE 8000
ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json
ENTRYPOINT ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8000", "--reload", "--worker-class", "eventlet","gator.flask:app"]
