import docker
import psutil
import time
import subprocess
import scheduler_logger

# Initialize Docker client
client = docker.from_env()
scheduler = scheduler_logger.SchedulerLogger()
memcached_cores = ""


def remove_container(containers):
    containers.reload()
    if containers.status == "exited":
        print(f"Removing container {containers.name}")
        print(f"Container {containers.name} exited with code {containers.attrs['State']['ExitCode']}")
        scheduler.job_end(job = containers.name)
        containers.remove()
        return True
    return False

def get_cpu_utilization(core):
    """Returns the CPU utilization percentage"""
    cpu_per = psutil.cpu_percent(interval=1, percpu=True)
    return cpu_per[core]

def get_pid(process_name):
    for proc in psutil.process_iter():
        if process_name in proc.name():
            return proc.pid
    return None

def adjust_memcached_resources(cpu_cores):
    global memcached_cores
    """Adjusts the CPU affinity of memcached using taskset command"""
    try:
        # Get PID of memcached
        pid = get_pid("memcached")
        # Execute taskset command
        subprocess.check_output(["sudo", "taskset", "-a", "-cp", f"{cpu_cores}", str(pid)])
        scheduler.update_cores(job = "memcached", cores = cpu_cores.split("-"))
        memcached_cores = cpu_cores
    except Exception as e:
        print(f"Failed to adjust memcached resources: {e}")


def create_job(job, cores, threads):
    """Runs a PARSEC job in a Docker container with specified cores"""
    try:
        if job["image"][0:3] == "spl":
            container = client.containers.create(image="anakli/cca:" + job["image"], 
                                          command="./run -a run -S splash2x -p " + job["name"] + " -i native -n "+ threads, 
                                          detach=True, 
                                          name=job["name"], 
                                          cpuset_cpus=cores,
                                          auto_remove=False)
        else:
            container = client.containers.create(image="anakli/cca:" + job["image"], 
                                          command="./run -a run -S parsec -p " + job["name"] + " -i native -n "+ threads, 
                                          detach=True, 
                                          name=job["name"], 
                                          cpuset_cpus=cores,
                                          auto_remove=False)
        container.reload()
        return container

    except Exception as e:
        print(f"Failed to create job {job}: {e}")

def start_job(container):
    """Starts a Docker container"""
    try:
        container.reload()
        if (container.status == "created"):
            container.start()
            container.reload()
            scheduler.job_start(job = container.name, initial_cores = container.attrs['HostConfig']['CpusetCpus'], initial_threads = 2 if len(container.attrs['HostConfig']['CpusetCpus']) > 1 else 1)
        return container
    except Exception as e:
        print(f"Failed to start job {container.name}: {e}")

def pause_job(container):
    """Pauses a Docker container"""
    try:
        container.pause()
        container.reload()
        scheduler.job_pause(job = container.name)
        return container
    except Exception as e:
        print(f"Failed to pause job {container.name}: {e}")

def unpause_job(container):
    """Resumes a Docker container"""
    try:
        container.unpause()
        container.reload()
        scheduler.job_unpause(job = container.name)
        return container
    except Exception as e:
        print(f"Failed to resume job {container.name}: {e}")

def update_job_cores(container, cores, update_log = False):
    """Updates the cores of a Docker container"""
    try:
        container.reload()
        if (container.status != "exited"):
            container.update(cpuset_cpus=cores)
            container.reload()
            if update_log:
                scheduler.update_cores(job = container.name, cores = cores)
        return container
    except Exception as e:
        print(f"Failed to update job cores {container.name}: {e}")


def main():
    global memcached_cores

    stop_update = False
    
    adjust_memcached_resources(cpu_cores="0")

    # Assume a list for the jobs and their properties
    jobs = [
        {"name": "canneal", "image": "parsec_canneal", "core": "1"},
        {"name": "vips", "image": "parsec_vips", "core": "1"},
        {"name": "blackscholes", "image": "parsec_blackscholes", "core": "1"},
        {"name": "dedup", "image": "parsec_dedup", "core": "1"},
        {"name": "radix", "image": "splash2x_radix", "core": "2,3"},
        {"name": "ferret", "image": "parsec_ferret", "core": "2,3"},
        {"name": "freqmine", "image": "parsec_freqmine", "core": "2,3"},
    ]
    
    # Store running containers
    containers_1 = []
    containers_23 = []

    print("Creating job groups...")
    for job in jobs:
        # Start a new thread to run the job
        cores = job["core"]
        if cores == "1":
            threads = "1"
        else:
            threads = "2"
        container = create_job(job, cores, threads)
        if cores == "1":
            containers_1.append((container, job))
        else:
            containers_23.append((container, job))
    print("Jobs created successfully...")

    while containers_1 or containers_23:
        if containers_1:
            cpu = get_cpu_utilization(0)
            if memcached_cores == "0":
                containers_1[0][0].reload()
                if cpu > 80:
                    if containers_1[0][0].status == "running":
                        pause_job(containers_1[0][0])
                    adjust_memcached_resources(cpu_cores="0-1")
                elif containers_1[0][0].status == "created":
                        start_job(containers_1[0][0])

            # If CPU utilization is low
            elif cpu + get_cpu_utilization(1) < 130:
                adjust_memcached_resources(cpu_cores="0")
                containers_1[0][0].reload()
                if containers_1[0][0].status == "paused":
                    unpause_job(containers_1[0][0])
                else:
                    start_job(containers_1[0][0])

        # Check if docker container finished    
        
            if remove_container(containers_1[0][0]):
                containers_1.pop(0)
        elif not stop_update:
            stop_update = True
            adjust_memcached_resources("0-1")

        if containers_23:
            if containers_23[0][0].status == "created":
                start_job(containers_23[0][0])
            if remove_container(containers_23[0][0]):
                containers_23.pop(0)
            if len(containers_23) > 1 and remove_container(containers_23[1][0]):
                containers_23.pop(1)
        else:
            if len(containers_1) > 2:
                container, job = containers_1.pop(0)
                containers_23.append((container, job))
                update_job_cores(container, "2", True)
                container.reload()
                if container.status == "paused":
                    unpause_job(container)
                container, job = containers_1.pop(0)
                containers_23.append((container, job))
                update_job_cores(container, "3")
                start_job(containers_23[1][0])
            elif len(containers_1) == 1:
                container, job = containers_1.pop(0)
                containers_23.append((container, job))
                update_job_cores(container, "2", True)
                container.reload()
                if container.status == "paused":
                    unpause_job(container)
                adjust_memcached_resources("0-1")
            elif len(containers_1) > 1:
                container, job = containers_1.pop(1)
                containers_23.append((container, job))
                update_job_cores(container, "2")
                start_job(containers_23[0][0])

    scheduler.custom_event(job="scheduler - ", comment="All job completed successfully. Running memcached...")
    adjust_memcached_resources("0-1")
    time.sleep(80)
    scheduler.custom_event(job="scheduler - ", comment="Memcached runned for 80 seconds. Ending scheduler...")
    scheduler.end()


if __name__ == "__main__":
    main()
