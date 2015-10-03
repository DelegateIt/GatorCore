FROM ubuntu:12.04
MAINTAINER Austin Middleton

RUN apt-get update
RUN apt-get install -y openjdk-7-jre-headless

##################
# Configurations #
##################

RUN addgroup --gid 4000 gator
RUN useradd --gid 4000 --no-create-home gator

EXPOSE 8040

ADD source /var/gator/db
WORKDIR /var/gator/db
ADD http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz dynamo.tar.gz
RUN tar -xzf dynamo.tar.gz

RUN chown -R gator:gator /var/gator/db
USER gator
ENTRYPOINT ["java", "-Djava.library.path=./DynamoDBLocal_lib", "-jar", "DynamoDBLocal.jar", "-sharedDb", "-delayTransientStatuses", "-port", "8040"]

