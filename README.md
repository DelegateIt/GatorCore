# GatorCore
This repo is responsible for the setup of the production/test environment of the backend api and delegator web server. The environment is setup using Docker so everyone will need that installed.

## Setup
The general work flow for setting up the environment is this:
 1. Install Docker
 2. Clone this repo then `cd` into it
 3. run `setupenv.py db` to create the docker iamge and container for the database
 4. run `setupenv.py api /path/to/api/source/code` to create the docker image and container for the api

To start the api run:
```
docker start -a db
docker start -a api
```
This will start the database container then the api container. It's important to start the database container first since the api container is dependent on the database.

To stop a container use `docker stop <container_name>`. A stopped container can be started agian using the above start command. All file state is saved across restarts. In order to start from scratch or update the image/container, the `setupenv.py` script has to be rerun.

The delegator web server image/container can also be created by running `setupenv.py delgt /path/to/delegator/source/code`

### Meta
The port mappings are as follows: 8000 for the api, 8040 for the db, and 8080 for the delegator web server.

For the `delg` and `api` containers, both required a path to their respective source code. When those files change on the host, they are immediatly reflected in the docker container. If for some reason you need to find those files from within the docker container, they are located in `/var/gator`.

### Extras
Sometimes it's neccessary to get a shell in a container and this command can be used `docker exec -t -i <container_name> /bin/bash`

To list all the containers and some info about them run `docker ps -a`.

There are a lot of other useful things docker can do and some of them are listed in the `docker --help` output.
