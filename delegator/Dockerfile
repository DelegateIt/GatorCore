FROM delegateit/gatbase
MAINTAINER Austin Middleton

RUN apt-get install -y nginx

ADD delegator-site.conf /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

ADD source /var/gator/delegator
WORKDIR /var/gator/delegator
EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]
