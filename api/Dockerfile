FROM ubuntu:12.04
MAINTAINER Austin Middleton

RUN apt-get update

#######################
# Production packages #
#######################

RUN apt-get install -y\
    python-pip\
    python-dev\
    libffi-dev\
    libssl-dev

#These are already installed and need to be upgraded
RUN pip install --upgrade\
    pip\
    boto

RUN pip install\
    Flask\
    gevent\
    gunicorn\
    jsonpickle\
    requests\
    stripe\
    twilio\
    urllib3\
    ndg-httpsclient

#########################
# Developement packages #
#########################

#RUN apt-get install -y openjdk-7-jre-headless

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
ENTRYPOINT ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8000", "--reload", "--worker-class", "gevent", "wsgi:app"]
