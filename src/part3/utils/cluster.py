import os
import sys
import subprocess
from utils.memcached import get_memcached_status
from utils.mcperf import install_mcperf, launch_mcperf

_cluster_name = "part3.k8s.local"
_machine_names = {}

def _check_env() -> bool:
    envs = ["KOPS_STATE_STORE", "PROJECT"]
    for env in envs:
        if env not in os.environ:
            print(f"Environment variable {env} not set. Please run `source env.sh`")
            return False
    return True

def _check_cluster_running() -> bool:
    command = f"kops validate cluster --name {_cluster_name}"
    if subprocess.run(command.split(), capture_output=True).returncode != 0:
        print("Cluster not running. Please run `python3 main.py create -f cluster.yaml`")
        return False
    return True

def _get_nodes_data():
    cmd = "kubectl get nodes -o wide"
    result = subprocess.run(cmd.split(), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {result.stderr}")
        sys.exit(1)
    lines = result.stdout.split('\n')
    column_names = lines[0].split()
    name_index = column_names.index('NAME')
    ip_index = column_names.index('INTERNAL-IP')
    nodes = {}
    for line in lines[1:]:
        if line:
            columns = line.split()
            name = columns[name_index]
            ip = columns[ip_index]
            nodes[name] = ip
    global _machine_names
    _machine_names = {k[:-5]: {"name": k, "ip": v} for k, v in nodes.items()}

def get_machine_names() -> dict:
    if len(_machine_names.items()) == 0:
        _get_nodes_data()
    return _machine_names

def get_status(print_status=False):
    if not _check_env():
        sys.exit(1)
    if print_status:
        print("Environment variables set ✅")
    if not _check_cluster_running():
        sys.exit(1)
    if print_status:
        print("Cluster running ✅")
    if len(_machine_names.items()) == 0:
        _get_nodes_data()
    if len(_machine_names.items()) == 0:
        print("0 nodes running ❌")
        sys.exit(1)
    if print_status:
        print(f"{len(_machine_names.items())} nodes running ✅")
        get_memcached_status(True)

def create_cluster(filename):
    if not _check_env():
        sys.exit(1)
    commands = [
        f"kops create -f {filename}",
        f"kops create secret --name {_cluster_name} sshpublickey admin -i ~/.ssh/cloud-computing-24.pub",
        f"kops update cluster --name {_cluster_name} --yes --admin",
        "kops validate cluster --wait 10m"
    ]
    print("Creating cluster... ")
    for command in commands:
        subprocess.run(command.split(), capture_output=True)
    print("Cluster created ✅")
    install_mcperf()

def delete_cluster():
    if not _check_env():
        sys.exit(1)
    command = f"kops delete cluster --name {_cluster_name} --yes"
    subprocess.run(command.split(), capture_output=True)
