#!/usr/bin/env python3

import sys
REQUIRED_PYTHON = (3, 4, 0)
if sys.version_info < REQUIRED_PYTHON:
    print("Please upgrade your version of python to at least v{}.{}.{}".format(*REQUIRED_PYTHON))
    exit(1)


import os
import argparse
import subprocess
import tempfile

USE_DOCKER_IO = False
DOCKER_COMMAND = "docker.io" if USE_DOCKER_IO else "docker"

def execute_no_fail(command, *args, **kwargs):
    return_code = execute(command, *args, **kwargs)
    if return_code != 0:
        raise Exception("The command {} returned {}".format(command, return_code))

def execute(command, cwd=None, shell=False):
    print("EXECUTING:", " ".join(command))
    return subprocess.Popen(command, cwd=cwd, shell=shell).wait()

class Start(object):

    @staticmethod
    def start_container(name):
        print("Starting {} container".format(name))
        return execute_no_fail([DOCKER_COMMAND, "start", name])

    @staticmethod
    def start_api_env():
        Start.start_container("db")
        Start.start_container("api")
        Start.start_container("ntfy")
        print("\nThe api is accessible from port 8000 and socket.io from 8060")

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Starts the api environment")
        parser.parse_args()
        Start.start_api_env()

class Stop(object):

    @staticmethod
    def stop_container(name, time_till_kill=3):
        print("Stopping {} container".format(name))
        return execute_no_fail([DOCKER_COMMAND, "stop", "-t", str(time_till_kill), name])

    @staticmethod
    def stop_api_env():
        Stop.stop_container("ntfy")
        Stop.stop_container("api")
        Stop.stop_container("db")

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Stops the api environment")
        parser.parse_args()
        Stop.stop_api_env()


class Create(object):

    @staticmethod
    def kill_and_delete(name):
       execute([DOCKER_COMMAND, "rm", "-f", name])

    @staticmethod
    def create_image(name, source, no_cache):
        args = [DOCKER_COMMAND, "build", "-t", name]
        if no_cache:
            args.append("--no-cache")
        args.append(source)
        execute_no_fail(args)

    @staticmethod
    def create_container(name, image, ports=None, volumes=None, links=None, tty=False, net="bridge"):
        command = [DOCKER_COMMAND, "create", "--name", name]
        if ports:
            for p in ports:
                command.extend(["-p", str(p[0]) + ":" + str(p[1])])
        if volumes:
            for v in volumes:
                command.extend(["-v", v[0] + ":" + v[1]])
        if links:
            for link in links:
                command.extend(["--link", link])
        if tty:
            command.append("-t")
        command.append("--net=" + net)
        command.append(image)
        execute(command)

    @staticmethod
    def setup_api_container(volume, no_cache):
        Create.kill_and_delete("api")
        Create.create_image("delegateit/gatapi", "api", no_cache)
        Create.create_container("api", "delegateit/gatapi",
                ports=[[8000, 8000]],
                volumes=[[volume, "/var/gator/api"]],
                net="host")

    @staticmethod
    def setup_ntfy_container(volume, no_cache):
        Create.kill_and_delete("ntfy")
        Create.create_image("delegateit/gatntfy", "notify", no_cache)
        Create.create_container("ntfy", "delegateit/gatntfy",
                ports=[[8060, 8060]],
                volumes=[[volume, "/var/gator/api"]],
                tty=True,
                net="host")

    @staticmethod
    def setup_db_container(volume, no_cache):
        Create.kill_and_delete("db")
        Create.create_image("gatdb", "db", no_cache)
        Create.create_container("db", "gatdb",
                ports=[[8040, 8040]],
                volumes=[[volume, "/var/gator/api"]],
                net="host")

    @staticmethod
    def setup_delgt_container(volume, no_cache):
        Create.kill_and_delete("delgt")
        Create.create_image("delegateit/gatdelgt", "delegator", no_cache)
        Create.create_container("delgt", "delegateit/gatdelgt",
                ports=[[8080, 8080]],
                volumes=[[volume, "/var/gator/delegator"]],
                net="host")

    @staticmethod
    def parse_args():
        containers = ["api", "db", "delgt", "ntfy", "fullapi"]
        parser = argparse.ArgumentParser(description="docker container and image creation for DelegateIt")
        parser.add_argument("name", choices=containers,
                help="the name of the container to create.")
        parser.add_argument("--no-cache", default=False, action="store_true", dest="no_cache",
                help="Do not use docker's cache when building images.")
        parser.add_argument("source",
                help="the location of the project's source code.")
        args = parser.parse_args()

        abs_source = ""
        if args.source != "":
            abs_source = os.path.abspath(args.source)
            if not os.path.isdir(abs_source):
                parser.print_help()
                print("\n\n'{}' is not a directory".format(abs_source))
                exit(1)

        Create.create_image("delegateit/gatbase", "base", args.no_cache)
        if args.name == "api" or args.name == "fullapi":
            Create.setup_api_container(abs_source, args.no_cache)
        if args.name == "db" or args.name == "fullapi":
            Create.setup_db_container(abs_source, args.no_cache)
        if args.name == "ntfy" or args.name == "fullapi":
            Create.setup_ntfy_container(abs_source, args.no_cache)
        if args.name == "delgt":
            Create.setup_delgt_container(abs_source, args.no_cache)

class Package(object):

    @staticmethod
    def package_lambda(apisource, apiconfig, outdir, tempdir):
        print("Packaging lambda")
        execute_no_fail(["cp", "-R", os.path.join(apisource, "notify"), tempdir])
        execute_no_fail(["cp", apiconfig, os.path.join(tempdir, "notify", "config.json")])
        execute_no_fail(["zip", "-r", os.path.join(os.getcwd(), outdir, "gatorlambda.zip"),
                "lambda.js",
                "gator.js",
                "config.json"],
                cwd=os.path.join(tempdir, "notify"))

    @staticmethod
    def package_fullapi(apisource, delgtsource, apiconfig, delgtconfig, outdir, tempdir):
        print("Packaging fullapi")
        execute_no_fail(["cp", "-R", apisource, os.path.join(tempdir, "apisource")])
        execute_no_fail(["cp", "-R", delgtsource, os.path.join(tempdir, "delgtsource")])
        execute_no_fail(["cp", apiconfig,
                os.path.join(tempdir, "apisource", "aws-prod-config.json")])
        execute_no_fail(["cp", delgtconfig,
                os.path.join(tempdir, "delgtsource", "www", "js", "config.js")])
        execute_no_fail(["cp", "Dockerrun.aws.json", tempdir])
        execute_no_fail(["zip", "-r", os.path.join(os.getcwd(), outdir, "gatorfullapi.zip"),
                "apisource",
                "delgtsource",
                "Dockerrun.aws.json",
                "-x", "*/.git/*", "*/__pycache__/*"], cwd=tempdir)

    @staticmethod
    def package_all(apisource, delgtsource, apiconfig, delgtconfig, outdir):
        with tempfile.TemporaryDirectory() as tempdir:
            api_temp = os.path.join(tempdir, "api")
            lambda_temp = os.path.join(tempdir, "lambda")
            execute_no_fail(["mkdir", api_temp])
            execute_no_fail(["mkdir", lambda_temp])
            Package.package_fullapi(apisource, delgtsource, apiconfig, delgtconfig, outdir, api_temp)
            Package.package_lambda(apisource, apiconfig, outdir, lambda_temp)

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
                description="Packages the environment for elastic beanstalk in a zip")
        parser.add_argument("-a", "--api", required=True,
                help="The source directory for the api")
        parser.add_argument("-d", "--delegator", required=True,
                help="The source directory for the delegator server")
        parser.add_argument("-c", "--aconfig", required=True,
                help="The config file for the api to use")
        parser.add_argument("-s", "--dconfig", required=True,
                help="The config file for the delegator client to use")
        parser.add_argument("-o", "--outdir", default=".",
                help="The folder to store the zip files")
        args = parser.parse_args()
        Package.package_all(args.api, args.delegator, args.aconfig, args.dconfig, args.outdir)

class DockerPush(object):
    @staticmethod
    def docker_push_list(image_list):
        for image in image_list:
            execute_no_fail([DOCKER_COMMAND, "push", image])

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
                description="Pushes all the production images to docker hub")
        DockerPush.docker_push_list([
                "delegateit/gatbase",
                "delegateit/gatapi",
                "delegateit/gatntfy",
                "delegateit/gatdelgt"])


if __name__ == "__main__":
    actions = {
        "create": {
            "parse": Create.parse_args,
            "description": "create the docker containers and images"
        },
        "start": {
            "parse": Start.parse_args,
            "description": "Starts the api environment"
        },
        "stop": {
            "parse": Stop.parse_args,
            "description": "Stops the api environment"
        },
        "package": {
            "parse": Package.parse_args,
            "description": "Packages the environment for elastic beanstalk in a zip"
        },
        "dockerpush": {
            "parse": DockerPush.parse_args,
            "description": "Pushes all the production images to docker hub"
        }
    }
    parser = argparse.ArgumentParser(
            description="Helps setup and control the environents for DelegateIt. Possible actions include: " +
            ". ".join([k + " - " + v["description"] for k,v in actions.items()]))
    parser.add_argument("action", choices=actions.keys(), help="The action to perform.")
    parser.add_argument('args', nargs=argparse.REMAINDER,
            help="A list of arguments to pass to the action")


    args = parser.parse_args()
    action_name = sys.argv[1]
    del sys.argv[1]
    sys.argv[0] += " " + args.action
    actions[action_name]["parse"]()
