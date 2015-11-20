# GatorCore
This repo is responsible for the setup of the production/test environment of the backend api and delegator web server. The environment is setup using Docker so everyone will need that installed.

#### Aside for mac and windoze users
Setting up docker in these environments is a little different since docker relies on features in the linux kernel to work properly. Docker should be installed using the Docker Toolkit which will create a linux vm for you then it'll run docker inside the vm. Since the vm uses a different network stack than the host, you cannot connect to the docker containers through `localhost`. Instead you must use the ip of the vm or port forward from `localhost` to the vm (which can be done easily through the vm's config gui). If you're using Windows™®, the system probably won't work at all, which should be the least of worries since your'e using Windows™®.

## Setup
The general work flow for setting up the environment is this:
 1. Install Docker
 2. Clone this repo then `cd` into it
 3. run `env.py create db` to create the docker iamge and container for the database
 4. run `env.py create api /path/to/api/source/code` to create the docker image and container for the api

To start the api run:
```
docker start -a db
docker start -a api
```
This will start the database container then the api container. It's important to start the database container first since the api container is dependent on the database.

To stop a container use `docker stop <container_name>`. A stopped container can be started agian using the above start command. All file state is saved across restarts. In order to start from scratch or update the image/container, the `env.py` script has to be rerun.

The delegator web server image/container can also be created by running `env.py delgt /path/to/delegator/source/code`

### Meta
The port mappings are as follows: 8000 for the api, 8040 for the db, and 8080 for the delegator web server.

For the `delgt` and `api` containers, both required a path to their respective source code. When those files change on the host, they are immediatly reflected in the docker container. If for some reason you need to find those files from within the docker container, they are located in `/var/gator`.

### Extras
Sometimes it's neccessary to get a shell in a container and this command can be used `docker exec -t -i <container_name> /bin/bash`. You might notice that by default you won't have sudo access since the default user has no password. If you need root access pass the `-u root` argument into docker exec like this `docker exec -t -i -u root <container_name> /bin/bash`

To list all the containers and some info about them run `docker ps -a`.

There are a lot of other useful things docker can do and some of them are listed in the `docker --help` output.
