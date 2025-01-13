import subprocess
from utils.ssh import ssh_exec

def install_mcperf():
    print("Installing mcperf...")
    machine_to_install = [
        "client-agent",
        "client-measure"
    ]
    cmd_install = "export DEBIAN_FRONTEND=noninteractive && \
        echo deb-src http://europe-west3.gce.archive.ubuntu.com/ubuntu/ bionic main restricted | sudo tee -a /etc/apt/sources.list > /dev/null && \
        sudo apt-get update >/dev/null 2>&1 && \
        sudo apt-get install libevent-dev libzmq3-dev screen git make g++ --yes > /dev/null 2>&1 && \
        sudo apt-get build-dep memcached --yes > /dev/null 2>&1 && \
        git clone https://github.com/eth-easl/memcache-perf-dynamic.git > /dev/null 2>&1 && \
        cd memcache-perf-dynamic >/dev/null 2>&1 && \
        make  >/dev/null 2>&1"
    for machine in machine_to_install:
        ssh_exec(machine, cmd_install)
        print(f"mcperf installed on {machine} ✅")

def _get_memcached_pod_ip():
    result = subprocess.run(['kubectl', 'get', 'node', 'some-memcached', '-o', 'jsonpath={.status.podIP}'], capture_output=True, text=True).stdout.strip()
    return result

def launch_mcperf(machine_names, file_name):
    killall_command = "killall mcperf > /dev/null 2>&1 &"
    agent_command = "/home/ubuntu/memcache-perf-dynamic/mcperf -T {0} -A > /dev/null &"
    measure_command = f"/home/ubuntu/memcache-perf-dynamic/mcperf -s {machine_names['memcache-server']['ip']} --loadonly; \
        /home/ubuntu/memcache-perf-dynamic/mcperf -s {machine_names['memcache-server']['ip']} -a {machine_names['client-agent']['ip']}  \
        --noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 1200 --qps_interval 10 --qps_min 5000 --qps_max 100000 > memcache/{file_name}.txt &"

    print("Launching mcperf...")
    ssh_exec('client-agent', killall_command)
    ssh_exec('client-agent', agent_command.format(16))
    print("mcperf launched on client-agent ✅")
   
    ssh_exec('client-measure', killall_command)
    ssh_exec('client-measure', measure_command)
    print("mcperf launched on client-measure ✅")
