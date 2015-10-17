FROM ubuntu:14.04
MAINTAINER Austin Middleton

RUN addgroup --gid 4000 gator
RUN useradd --gid 4000 --no-create-home gator

EXPOSE 8080

ADD source /var/gator/delegator

USER gator
WORKDIR /var/gator/delegator
ENTRYPOINT ["python3.4", "/var/gator/delegator/startserver.py", "--port", "8080"]

