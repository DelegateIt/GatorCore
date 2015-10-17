FROM ubuntu:14.04
MAINTAINER Austin Middleton

RUN apt-get update

#######################
# Production packages #
#######################

RUN apt-get install -y python3-pip

#pip is installed but needs to upgraded because the apt repo is behind
RUN pip3 install --upgrade pip

#the upgrade version of pip runs as `pip` NOT `pip3`
RUN pip install\
    boto\
    Flask\
    eventlet\
    gunicorn\
    jsonpickle\
    requests\
    stripe\
    twilio

##################
# Configurations #
##################

RUN addgroup --gid 4000 gator
RUN useradd --gid 4000 --no-create-home gator

EXPOSE 8000

ADD source /var/gator/api

ENV GATOR_CONFIG_PATH=/var/gator/api/local-config.json

WORKDIR /var/gator/api
USER gator
ENTRYPOINT ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8000", "--reload", "--worker-class", "eventlet","gator:app"]
