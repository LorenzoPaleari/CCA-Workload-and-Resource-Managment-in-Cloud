import subprocess
import sys
import os
from utils.ssh import ssh_exec



def install_memcached():
    print("Installing memcached...")
    machine_to_install = [
        "memcache-server",
    ]
    cmd_install = "sudo apt update && sudo apt-get install -y memcached"
    for machine in machine_to_install:
        ssh_exec(machine, cmd_install)
        print(f"mcperf installed on {machine} ✅")
    
    command = 'echo "-t " | sudo tee -a /etc/memcached.conf'
    ssh_exec("memcache-server",command)


def configure_memcached(number_of_threads, machine_names):
    # commands to configure memcached
    machine_to_install =  "memcache-server"
    your_internal_ip = machine_names[machine_to_install]['ip']
    commands = [
        'sudo sed -i "s/-m .*/-m 1024/" /etc/memcached.conf',
        f'sudo sed -i "s/-l .*/-l {your_internal_ip}/" /etc/memcached.conf',
        f'sudo sed -i "s/-t .*/-t {number_of_threads}/" /etc/memcached.conf',
        "sudo systemctl restart memcached"
    ]
    
    for command in commands:
        ssh_exec(machine_to_install, command)



def get_memcached_status(print_status: bool = False) -> bool:
    command = "sudo systemctl status memcached"
    ssh_exec("memcache-server",command)
    return True
