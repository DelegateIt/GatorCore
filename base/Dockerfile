FROM ubuntu:14.04
MAINTAINER Austin Middleton

RUN apt-get update
RUN apt-get upgrade -y

#######################
# Production packages #
#######################

RUN apt-get install -y\
    python3-pip

#pip is installed but needs to upgraded because the apt repo is behind
RUN pip3 install --upgrade pip

#the upgrade version of pip runs as `pip` NOT `pip3`
RUN pip install\
    boto\
    jsonpickle\
    requests\
    nose

##################
# Configurations #
##################

RUN addgroup --gid 4000 gator
RUN useradd --gid 4000 --no-create-home gator

ENTRYPOINT ["/bin/bash"]
