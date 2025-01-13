#!/usr/bin/env python3

import argparse
import os
import importlib
import sys
import subprocess

from utils.cluster import get_status, create_cluster, delete_cluster, get_machine_names
from utils.memcached import launch_memcached, get_memcached_status, stop_memcached
from utils.timeparser import get_time

result_file = "results.json"

def test_runner(name, dirname):
    stop_memcached()
    launch_memcached("yaml/memcache-t1-cpuset.yaml")
    if not get_memcached_status():
        print("Memcached not running ❌")
        sys.exit(1)
    from utils.mcperf import launch_mcperf
    machine_names = get_machine_names()
    launch_mcperf(machine_names)
    
    module = importlib.import_module("schedulers." + name)
    print(f"Running {name} scheduler")
    module.main(dirname)
    print("Scheduler completed successfully ✅")
    
    command = "kubectl get pods -o json"
    output = subprocess.run(command.split(), capture_output=True, text=True)
    with open(result_file, "w") as f:
        f.write(output.stdout)
    print(f"Results written to {result_file} ✅")
    
    command = "kubectl delete jobs --all"
    subprocess.run(command.split(), capture_output=True)
    print("Jobs deleted ✅")

def analyze_results(dirname):
    get_time(dirname + result_file)

def check_file_exists(filename):
    if not os.path.isfile(filename):
        print(f'File {filename} does not exist ❌')
        return False
    return True

def check_dir_exists(dirname):
    if not os.path.isdir(dirname):
        print(f'Directory {dirname} does not exist ❌')
        return False
    return True

def main():
    parser = argparse.ArgumentParser(prog='main', description='Command line interface for cluster operations')
    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser('create', help='create cluster')
    create_parser.add_argument('-f', '--file', type=str, required=True, help='YAML file for cluster configuration')

    status_parser = subparsers.add_parser('status', help='get status')
    status_parser.add_argument('service', type=str, nargs='?', default=None, choices=['memcached'], help='Name of the service')

    start_parser = subparsers.add_parser('start', help='start service')
    start_parser.add_argument('service', type=str, choices=['memcached'], help='Name of the service')
    start_parser.add_argument('-f', '--file', type=str, required=True, help='File for memcached')

    stop_parser = subparsers.add_parser('stop', help='stop service')
    stop_parser.add_argument('service', type=str, choices=['memcached'], help='Name of the service')

    destroy_parser = subparsers.add_parser('destroy', help='destroy cluster')
    destroy_parser.add_argument('-y', '--yes', action='store_true', help='Confirm destruction of the cluster')

    ssh_parser = subparsers.add_parser('ssh', help='ssh to a node')
    ssh_parser.add_argument('name', type=str, help='Name of the node to connect')

    test_parser = subparsers.add_parser('test', help='test a scheduler')
    test_parser.add_argument('-s', '--s-name', type=str, required=True, help='Name for schefuler')
    test_parser.add_argument('-p', '--dir', type=str, required=True, help='Directory for parsec jobs')

    time_parser = subparsers.add_parser('time', help='analyze results')
    time_parser.add_argument('-r', '--dir_name', type=str, required=True, help='Directory for parsec jobs')

    args = parser.parse_args()
    service_not_recognized = 'Service not recognized.'
    if args.command == 'create':
        if check_file_exists(args.file):
            create_cluster(args.file)
    elif args.command == 'status':
        if args.service == 'memcached':
            get_memcached_status(True)
        elif args.service is None:
            get_status(True)
        else:
            print(service_not_recognized)
    elif args.command == 'stop':
        if args.service == 'memcached':
            stop_memcached()
        else:
            print(service_not_recognized)
    elif args.command == 'start':
        if args.service == 'memcached' and check_file_exists(args.file):
            launch_memcached(args.file)
        else:
            print(service_not_recognized)
    elif args.command == 'destroy':
        if args.yes or input('Are you sure you want to destroy the cluster? (y/n) ') == 'y':
            delete_cluster()
    elif args.command == 'ssh':
        from utils.ssh import ssh_launch
        ssh_launch(args.name)
    elif args.command == 'test':
        if check_dir_exists(args.dir) and check_file_exists(os.path.join('schedulers', args.s_name + '.py')):
            test_runner(args.s_name, args.dir)
    elif args.command == 'time':
        analyze_results(args.dir_name)
    else:
        print('No command specified. Use -h for help.')

if __name__ == '__main__':
    main()
