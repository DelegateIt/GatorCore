# GatorCore
The core backend product for DelegateIt

## Set up
* First clone the repo into any directoy of your choice and cd into it
* clone the rest api repo into the `shared/api` directory. `git clone https://github.com/DelegateIt/GatorRestService shared/api`
* clone the delegator web client repo into the `shared/web` directory. `git clone https://github.com/DelegateIt/GatorWebClient shared/web`
* install vagrant and virtualbox `sudo apt-get install vagrant virtualbox` for apt based systems
* run `vagrant up && vagrant reload`. This will startup the vm.
  * The very first time this is run, the vm is downloaded, then setup according to the configs automatically
* Thats everything. The web api should be accessible through port 8000 and the delegator web server through 8080.

### More info
The `shared/api` and `shared/web` directory is synced so changes made to it will be automatically reflected by the vm.

To shutdown the vm run `vagrant halt`, to start it up again use `vagrant up`, and to ssh into the vm use `vagrant ssh`.
If it asks for a password the default is 'vagrant'

#### TODO
There is still a lot to do before this is considered production ready, much less dev ready.

For production ready:
* for production we don't want to have to clone the api repo manually every time so we need to find a way to automate this

For dev ready:
* enable support for local running dynamodb

