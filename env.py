#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys

USE_DOCKER_IO = False
DOCKER_COMMAND = "docker.io" if USE_DOCKER_IO else "docker"

def execute_no_fail(command):
    return_code = execute(command)
    if return_code != 0:
        raise Exception("The command {} returned {}".format(command, return_code))

def execute(command):
    print("EXECUTING {}".format(command))
    if USE_DOCKER_IO:
        return subprocess.call(command, stdin=sys.stdin, stdout=sys.stdout)
    else:
        return subprocess.call(" ".join(command), stdin=sys.stdin, stdout=sys.stdout, shell=True)

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
    def setup_db_container(no_cache):
        Create.kill_and_delete("db")
        Create.create_image("gatdb", "db", no_cache)
        Create.create_container("db", "gatdb",
                ports=[[8040, 8040]],
                net="host")

    @staticmethod
    def setup_delgt_container(volume, no_cache):
        Create.kill_and_delete("delgt")
        Create.create_image("gatdelgt", "delegator", no_cache)
        Create.create_container("delgt", "gatdelgt",
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
        parser.add_argument("source", default="", nargs="?",
                help="the location of the project's source code. Required for all except for the `db` container")
        args = parser.parse_args()

        if args.name != "db" and args.source == "":
            parser.print_help()
            print("\n\n'{}' requires the path to the source files".format(args.name))
            exit(1)

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
            Create.setup_db_container(args.no_cache)
        if args.name == "ntfy" or args.name == "fullapi":
            Create.setup_ntfy_container(abs_source, args.no_cache)
        if args.name == "delgt":
            Create.setup_delgt_container(abs_source, args.no_cache)


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
