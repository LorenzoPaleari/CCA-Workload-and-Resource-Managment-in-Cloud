import subprocess
import time
import concurrent.futures
import sys
import os

_job_groups = [
    ["parsec-blackscholes"],
    ["parsec-dedup"],
    ["parsec-canneal"],
    ["parsec-ferret"],
    ["parsec-freqmine"],
    ["parsec-vips"],
    ["parsec-radix"]
]

def _wait_for_job(job):
    while True:
        result = subprocess.run(["kubectl", "get", "jobs", job], capture_output=True, text=True, check=True)

        lines = result.stdout.splitlines()
        if len(lines) < 2:
            print(f"Unexpected output for 'kubectl get jobs {job}': {result.stdout}")
            sys.exit(1)

        completions = lines[1].split()[1]
        if completions == "1/1":
            break
        time.sleep(1)

def _run_job_group(job_group, dirname):
    for job in job_group:
        subprocess.run(["kubectl", "create", "-f", f"{os.path.join(dirname, job)}.yaml"], check=True)
        _wait_for_job(job)

def main(dirname):
    dir_list = [dirname] * len(_job_groups)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(_run_job_group, _job_groups, dir_list)
    print("All job groups completed successfully.")
