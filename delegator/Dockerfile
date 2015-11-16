FROM ubuntu:14.04
MAINTAINER Austin Middleton

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y nginx


ADD delegator-site.conf /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default
ADD source /var/gator/delegator


# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 8080
WORKDIR /var/gator/delegator
ENTRYPOINT ["nginx", "-g", "daemon off;"]

