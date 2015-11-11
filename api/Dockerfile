FROM gatbase
MAINTAINER Austin Middleton

#######################
# Production packages #
#######################

RUN pip install\
    Flask\
    eventlet\
    gunicorn\
    stripe\
    twilio

##################
# Configurations #
##################

EXPOSE 8000

ADD source /var/gator/api

ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json

WORKDIR /var/gator/api
USER gator
ENTRYPOINT ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8000", "--reload", "--worker-class", "eventlet","gator.flask:app"]
