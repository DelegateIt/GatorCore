#!/usr/bin/env python2.7

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

def kill_and_delete(name):
   execute(["docker", "rm", "-f", name])

def create_image(name, source):
    execute_no_fail(["docker", "build", "-t", name, source])

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

def setup_api_container(volume):
    kill_and_delete("api")
    create_image("gatapi", "api")
    create_container("api", "gatapi",
            ports=[[8000, 8000]],
            volumes=[[volume, "/var/gator/api"]],
            net="host")

def setup_ntfy_container(volume):
    kill_and_delete("ntfy")
    create_image("gatntfy", "notify")
    create_container("ntfy", "gatntfy",
            ports=[[8060, 8060]],
            volumes=[[volume, "/var/gator/api"]],
            tty=True,
            net="host")

def setup_db_container():
    kill_and_delete("db")
    create_image("gatdb", "db")
    create_container("db", "gatdb",
            ports=[[8040, 8040]],
            net="host")

def setup_delgt_container(volume):
    kill_and_delete("delgt")
    create_image("gatdelgt", "delegator")
    create_container("delgt", "gatdelgt",
            ports=[[8080, 8080]],
            volumes=[[volume, "/var/gator/delegator"]],
            net="host")

if __name__ == "__main__":
    containers = ["api", "db", "delgt", "ntfy"]
    parser = argparse.ArgumentParser(description="docker enviroment setup for DelegateIt")
    parser.add_argument("name",
            help="the name of the container to create. Valid options are " + str(containers))
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
        setup_api_container(abs_source)
    elif args.name == "delgt":
        setup_delgt_container(abs_source)
    elif args.name == "db":
        setup_db_container()
    elif args.name == "ntfy":
        setup_ntfy_container(abs_source)

