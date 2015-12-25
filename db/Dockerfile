FROM delegateit/gatbase
MAINTAINER Austin Middleton

RUN apt-get install -y\
    openjdk-7-jre-headless\
    wget

ADD source /var/gator/db
WORKDIR /var/gator/db

RUN wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz
RUN tar -xzf dynamodb_local_latest.tar.gz
RUN chown -R gator:gator /var/gator/db

USER gator
EXPOSE 8040
ENTRYPOINT ["java", "-Djava.library.path=./DynamoDBLocal_lib", "-jar", "DynamoDBLocal.jar", "-sharedDb", "-delayTransientStatuses", "-port", "8040"]
