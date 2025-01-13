import subprocess
import sys
import os

def launch_memcached(filename):
    if not get_memcached_status():
        commands = [
        f"kubectl create -f {filename}",
        "kubectl expose pod some-memcached --name some-memcached-11211 --type LoadBalancer --port 11211 --protocol TCP ",
        "sleep 10 "
        ]
        returncode = 0
        for command in commands:
            returncode += subprocess.run(command.split(), capture_output=True).returncode
        if returncode > 0:
            print("Memcached launch failed ❌")
            sys.exit(1)
        else:
            print("Memcached launched ✅")
    else:
        print("Memcached already running ❌")

def get_memcached_status(print_status: bool = False) -> bool:
    command = "kubectl get pods 2>&1 | grep memcached | grep Running > /dev/null 2>&1"
    running = os.system(command) == 0
    if running and print_status:
        print('Memcached is running ✅')
    elif print_status:
        print('Memcached is not running ❌')
    return running

def stop_memcached():
    commands = [
        "kubectl delete pods some-memcached",
        "kubectl delete service some-memcached-11211"
        ]
    for command in commands:
        subprocess.run(command.split(), capture_output=True)
    print("Memcached stopped ✅")
