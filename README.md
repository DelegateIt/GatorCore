# GatorCore
This repo is responsible for the setup of the production/test environment of the backend api and delegator web server. The environment is setup using Docker so you will need that installed.

#### Aside for mac and windoze users
Setting up docker in these environments is a little different since docker relies on features in the linux kernel to work properly. Docker should be installed using the [Docker Toolbox](https://www.docker.com/docker-toolbox) which will create a linux vm for you then it'll run docker inside the vm. The Toolbox comes with a program called "Docker Quickstart Terminal" that will open your default shell and configure it with the correct environment variables for docker to work. It also ensures your linux vm is configured and running. All the below commands should be run inside the terminal that "Docker Quickstart Termainal" opens.

## Setup
The general work flow for setting up the environment is this:
 1. Install Docker or the Docker Toolbox if you use a mac
 2. Clone this repo then `cd` into it
 3. run `env.py create fullapi /path/to/api/source/code` to create the neccessary docker containers to run the api. The directory for the source of the OrderApi should be provided as an argument.

To stat the api run `env.py start`. To stop it run `env.py stop`. The environment can be started again using the 'start' action without having to re-run the 'create' action. All file state is saved across restarts. In order to start from scratch or update the image/container, the 'create' action must be re-run.

### Meta
Port mappings:
 * 8000: Flask API
 * 8040: DB
 * 8060: Socket.io


 The ip address for the docker containers is `127.0.0.1` on linux and for macs it is whatever ip your vm is assigned. The "Docker Quickstart Terminal" will print out this ip when it is opened. Alternatively, the command `docker-machine ip default` will print out the ip.

### Extras
Sometimes it's neccessary to get a shell in a container and this command can be used `docker exec -t -i <container_name> /bin/bash`. You might notice that by default you won't have sudo access since the default user has no password. If you need root access pass the `-u root` argument into docker exec like this `docker exec -t -i -u root <container_name> /bin/bash`

To list all the containers and some info about them run `docker ps -a`.

There are a lot of other useful things docker can do and some of them are listed in the `docker --help` output.

### Troubleshooting
If you don't have internet access from the container you will need to get a shell and replace the default DNS entry in /etc/resolv.conf to Google's DNS (8.8.8.8)
