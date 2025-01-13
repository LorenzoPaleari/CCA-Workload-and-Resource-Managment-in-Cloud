#!/usr/bin/env python3

import argparse
import os
import time
import sys
import subprocess
import re

from utils.cluster import get_status, create_cluster, delete_cluster, get_machine_names, get_machine_names_ext
from utils.memcached import get_memcached_status, install_memcached, configure_memcached
from utils.mcperf import launch_mcperf
from utils.timeparser import get_time
from utils.ssh import ssh_exec, ssh_exec_out, ssh_exec_out_no_check


result_file = "results.json"

def test_runner(name, file_name):
    machine_names_ext = get_machine_names_ext()
    machine_names = get_machine_names()

    # Kill all existing docker containers
    ssh_exec("memcache-server", "docker kill $(docker ps -q)")
    ssh_exec("memcache-server", "docker rm $(docker ps -aq)")
    ssh_exec("memcache-server", "docker kill $(docker ps -q)")
    ssh_exec("memcache-server", "docker rm $(docker ps -aq)")

    print("Copying scheduler to memcached server...")
    command = f"scp -i ~/.ssh/cloud-computing-24 ./schedulers/dynamic.py ubuntu@{machine_names_ext['memcache-server']['ip']}:~/"
    command2 = f"scp -i ~/.ssh/cloud-computing-24 ./schedulers/scheduler_logger.py ubuntu@{machine_names_ext['memcache-server']['ip']}:~/"
    output = subprocess.run(command.split(), capture_output=False, text=True)
    print("Scheduler copied ✅")
    output = subprocess.run(command2.split(), capture_output=True, text=True)
    print("Logger copied ✅")

    configure_memcached(2, machine_names)
    launch_mcperf(machine_names, file_name)
        
    print(f"Running {name} scheduler")
    ssh_exec_out_no_check("memcache-server", "taskset -a -c  3 python3 -u dynamic.py")
    print("Scheduler completed successfully ✅")

    
    # killall_command = "killall mcperf > /dev/null 2>&1 &"
    # ssh_exec("client-agent", killall_command)
    # ssh_exec("client-measure", killall_command)
    # print("mcperf stopped successfully ✅")

def analyze_results(dir_name):
    machine_names_ext = get_machine_names_ext()

    print("Copying log to local machine...")
    command = f"scp -r -i ~/.ssh/cloud-computing-24 ubuntu@{machine_names_ext['memcache-server']['ip']}:~/log ./results/{dir_name}/"
    output = subprocess.run(command.split(), capture_output=False, text=True)
    command2 = f"scp -r -i ~/.ssh/cloud-computing-24 ubuntu@{machine_names_ext['client-measure']['ip']}:~/memcache ./results/{dir_name}/"
    output = subprocess.run(command2.split(), capture_output=False, text=True)
    # Take finish time and start time and compute the difference

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

    destroy_parser = subparsers.add_parser('destroy', help='destroy cluster')
    destroy_parser.add_argument('-y', '--yes', action='store_true', help='Confirm destruction of the cluster')

    ssh_parser = subparsers.add_parser('ssh', help='ssh to a node')
    ssh_parser.add_argument('name', type=str, help='Name of the node to connect')

    test_parser = subparsers.add_parser('test', help='test a scheduler')
    test_parser.add_argument('-s', '--s-name', type=str, required=True, help='Name for schefuler')
    test_parser.add_argument('-o', '--file_name', type=str, required=True, help='Name for schefuler')

    time_parser = subparsers.add_parser('time', help='analyze results')
    time_parser.add_argument('-r', '--dir', type=str, required=True, help='Name of folder in which to store results')

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
    elif args.command == 'destroy':
        if args.yes or input('Are you sure you want to destroy the cluster? (y/n) ') == 'y':
            delete_cluster()
    elif args.command == 'ssh':
        from utils.ssh import ssh_launch
        ssh_launch(args.name)
    elif args.command == 'test':
        if check_file_exists(os.path.join('schedulers', args.s_name + '.py')):
            test_runner(args.s_name, args.file_name)
    elif args.command == 'time':
        if check_dir_exists(os.path.join('results', args.dir)):
            analyze_results(args.dir)
    else:
        print('No command specified. Use -h for help.')

if __name__ == '__main__':
    main()