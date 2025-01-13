import json
from datetime import datetime
import re

time_format = '%Y-%m-%dT%H:%M:%SZ'
for i in range (3,4):
    #Open the file in folder 1 and read the data
    file = open("./Runs/"+str(i)+"/results.json", "r")
    json_file = json.load(file)
    file.close()

    job_start_times = []
    job_completition_times = []
    names = []
    for item in json_file['items']:
        name = item['status']['containerStatuses'][0]['name']
        if str(name) != "memcached":
            start_time = datetime.strptime(
                        item['status']['containerStatuses'][0]['state']['terminated']['startedAt'],
                        time_format).timestamp()
            completion_time = datetime.strptime(
                        item['status']['containerStatuses'][0]['state']['terminated']['finishedAt'],
                        time_format).timestamp()
            names.append(name.split("-")[1])
            job_start_times.append(start_time)
            job_completition_times.append(completion_time)
    
    min_start_time = min(job_start_times)
    for j in range(len(job_start_times)):
        job_start_times[j] = job_start_times[j] - min_start_time
        job_completition_times[j] = job_completition_times[j] - min_start_time

    file = open("./Runs/"+str(i)+"/Job_run_" + str(i - 1) + ".csv", "w")
    file.write("Job,Start,End\n")
    for k in range(len(names)):
        file.write(names[k] + "," + str(job_start_times[k]) + "," + str(job_completition_times[k]) + "\n")
    file.close()

    #NOW We want also memcached results
    file = open("./Runs/"+str(i)+"/output.txt", "r")
    lines = file.readlines()
    file.close()

    p95 = []
    start_time = []
    end_time = []

    p95_index = re.split("\s+", lines[0]).index("p95")
    start_time_index = re.split("\s+", lines[0]).index("ts_start")
    end_time_index = re.split("\s+", lines[0]).index("ts_end")
    for line in lines[1:]:
        numbers = re.split("\s+", line)
        p95.append(float(numbers[p95_index]))
        start_time.append(float(numbers[start_time_index])/1000.0 - min_start_time - 7200 if float(numbers[start_time_index])/1000.0 - min_start_time - 7200 > 0 else 0) #2 hours of difference
        end_time.append(float(numbers[end_time_index])/1000.0 - min_start_time - 7200 if float(numbers[end_time_index])/1000.0 - min_start_time - 7200 > 0 else 0) #2 hours of difference
    
    max_end_time = max(job_completition_times)
    j = 0
    for j in range(len(start_time)):
        if start_time[j] > max_end_time:
            break

    p95 = p95[:j+1]
    start_time = start_time[:j+1]
    end_time = end_time[:j+1]

    file = open("./Runs/"+str(i)+"/memcached_run_" + str(i - 1) + ".csv", "w")
    file.write("Start,End,p95\n")
    for k in range(len(p95)):
        file.write(str(start_time[k]) + "," + str(end_time[k]) + "," + str(p95[k]) + "\n")
    file.close()
