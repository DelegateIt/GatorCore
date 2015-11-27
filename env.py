#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys

def execute_no_fail(command):
    return_code = execute(command)
    if return_code != 0:
        raise Exception("The command {} returned {}".format(command, return_code))

def execute(command):
    print("EXECUTING {}".format(command))
    return subprocess.call(command, stdin=sys.stdin, stdout=sys.stdout)

class Create(object):

    @staticmethod
    def kill_and_delete(name):
       execute(["docker", "rm", "-f", name])

    @staticmethod
    def create_image(name, source, no_cache):
        args = ["docker", "build", "-t", name]
        if no_cache:
            args.append("--no-cache")
        args.append(source)
        execute_no_fail(args)

    @staticmethod
    def create_container(name, image, ports=None, volumes=None, links=None, tty=False, net="bridge"):
        command = ["docker", "create", "--name", name]
        if ports:
            for p in ports:
                command.extend(["-p", str(p[0]) + ":" + str(p[1])])
        if volumes:
            for v in volumes:
                command.extend(["-v", v[0] + ":" + v[1] + ":ro"])
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
        Create.create_image("gatapi", "api", no_cache)
        Create.create_container("api", "gatapi",
                ports=[[8000, 8000]],
                volumes=[[volume, "/var/gator/api"]],
                net="host")

    @staticmethod
    def setup_ntfy_container(volume, no_cache):
        Create.kill_and_delete("ntfy")
        Create.create_image("gatntfy", "notify", no_cache)
        Create.create_container("ntfy", "gatntfy",
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
    def setup_delgt_container(volume):
        Create.kill_and_delete("delgt")
        Create.create_image("gatdelgt", "delegator", no_cache)
        Create.create_container("delgt", "gatdelgt",
                ports=[[8080, 8080]],
                volumes=[[volume, "/var/gator/delegator"]],
                net="host")

    @staticmethod
    def parse_args():
        containers = ["api", "db", "delgt", "ntfy"]
        parser = argparse.ArgumentParser(description="docker container and image creation for DelegateIt")
        parser.add_argument("name",
                help="the name of the container to create. Valid options are " + str(containers))
        parser.add_argument("--no-cache", default=False, action="store_true", dest="no_cache",
                help="Do not use docker's cache when building images.")
        parser.add_argument("source", nargs="?", default="",
                help="the location of the project's source code. Required for all except for the `db` container")
        args = parser.parse_args()

        if not args.name in containers:
            parser.print_help()
            print("\n\n'{}' is not a valid container name. Must be one of these {}", args.name, containers)
            exit(1)

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

        if args.name == "api":
            Create.setup_api_container(abs_source, args.no_cache)
        elif args.name == "delgt":
            Create.setup_delgt_container(abs_source, args.no_cache)
        elif args.name == "db":
            Create.setup_db_container(args.no_cache)
        elif args.name == "ntfy":
            Create.setup_ntfy_container(abs_source, args.no_cache)


if __name__ == "__main__":
    actions = {
        "create": {
            "parse": Create.parse_args,
            "description": "create the docker containers and images"
        }
    }
    parser = argparse.ArgumentParser(
            description="Helps setup and control the environents for DelegateIt. Possible actions include: " +
            ". ".join([k + " - " + v["description"] for k,v in actions.items()]))
    parser.add_argument("action", help="The action to perform. Must be one of these: " + ",".join(actions.keys()))
    parser.add_argument('args', nargs=argparse.REMAINDER,
            help="A list of arguments to pass to the action")


    args = parser.parse_args()
    action_name = sys.argv[1]
    del sys.argv[1]
    sys.argv[0] += " " + args.action
    actions[action_name]["parse"]()
