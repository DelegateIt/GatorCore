FROM delegateit/gatbase
MAINTAINER Austin Middleton

RUN apt-get install -y nginx

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443

ENTRYPOINT ["nginx", "-g", "daemon off;"]
