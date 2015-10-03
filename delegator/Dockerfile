FROM ubuntu:12.04
MAINTAINER Austin Middleton

RUN apt-get update

RUN apt-get install -y python3

RUN addgroup --gid 4000 gator
RUN useradd --gid 4000 --no-create-home gator

EXPOSE 8080

ADD source /var/gator/delegator

USER gator
WORKDIR /var/gator/delegator
ENTRYPOINT ["python3", "/var/gator/delegator/startserver.py", "--port", "8080"]

