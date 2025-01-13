import os
import sys

def _check_name(name):
    from utils.cluster import get_machine_names
    machine_names = get_machine_names()
    if name not in machine_names:
        print(f"Machine {name} not found ❌")
        print("Available machines:")
        for machine in machine_names:
            print(f"\t{machine}")
        sys.exit(1)
    return machine_names[name]['name']

def ssh_launch(name):
    name_checked = _check_name(name)
    os.system(f"gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing-24 ubuntu@{name_checked} --zone europe-west3-a")

def ssh_exec(name, command):
    name_checked = _check_name(name)
    os.system(f"gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing-24 ubuntu@{name_checked} --zone europe-west3-a --command '{command}' > /dev/null 2>&1")
