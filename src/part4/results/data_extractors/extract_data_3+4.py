import os
from datetime import datetime
import re

folders = ["part3", "part4"]

for folder in folders:
    for i in range (1, 4):
        for file_name in sorted(os.listdir("../" + folder + "/" + str(i))):
            times = {}
            if "log" in file_name:
                file = open("../" + folder + "/" + str(i) + "/" + file_name, "r")
                lines = file.readlines()
                file.close()

                for j in range(len(lines)):
                    lines[j] = lines[j].split()
                    lines[j][0] = datetime.fromisoformat(lines[j][0]).timestamp()

                min_time = lines[2][0]
                max_time = lines[-5][0]
                complete_end_time = lines[-1][0]

                times["memcached"] = [[],[]]
                
                for line in lines:
                    if any(word in line[1] for word in ["start", "end", "pause", "unpause"]) and "scheduler" not in line[2]:
                        if "start" in line[1]:
                            times[line[2]] = [line[0] - min_time]
                        else:
                            times[line[2]].append(line[0] - min_time)
                
                times["memcached"][0].append(lines[1][0] - min_time if lines[1][0] - min_time > 0 else 0)
                times["memcached"][1].append(1)

                last = 1
                for line in lines[2:]:
                    if "update_cores" in line[1] and "memcached" in line[2]:
                        times["memcached"][0].append(line[0] - min_time if line[0] - min_time > 0 else 0)
                        if last == 2 and line[3] == "[0,1]":
                            times["memcached"][1].append(2)
                        elif last == 1:
                            times["memcached"][0].append(line[0] - min_time if line[0] - min_time > 0 else 0)
                            times["memcached"][1].append(1) 
                            times["memcached"][1].append(2)
                            last = 2
                        else:
                            times["memcached"][0].append(line[0] - min_time if line[0] - min_time > 0 else 0)
                            times["memcached"][1].append(2)
                            times["memcached"][1].append(1)
                            last = 1

                times["memcached"][0].append(complete_end_time - min_time)
                times["memcached"][1].append(2)

                file = open("../" + folder + "/" + str(i) + "/memcache_cores.csv", "w")
                file.write("time,core\n")
                for j in range(len(times["memcached"][0])):
                    file.write(str(times["memcached"][0][j]) + "," + str(times["memcached"][1][j]) + "\n")
                file.close()

                file = open("../" + folder + "/" + str(i) + "/jobs_time.csv", "w")
                to_write = ""
                max_lenght = 0
                for key in times:
                    if key != "memcached":
                        to_write += key + ","
                        if max_lenght < len(times[key]):
                            max_lenght = len(times[key])
                file.write(to_write[:-1] + "\n")
                for j in range(max_lenght):
                    to_write = ""
                    for key in times:
                        if key != "memcached":
                            if j < len(times[key]):
                                to_write += str(times[key][j]) + ","
                            else:
                                to_write += ","
                    file.write(to_write[:-1] + "\n")
                file.close()

                file = open("../" + folder + "/" + str(i) + "/output.txt", "r")
                lines = file.readlines()
                file.close()

                for j in range(6):
                    lines[j] = lines[j].split()
                
                ts_start = float(lines[3][2]) / 1000.0 - min_time - 7200
                ts_end = float(lines[4][2]) / 1000.0 - min_time - 7200

                step = (ts_end - ts_start) / 79 if folder == "part3" else (ts_end - ts_start) / 133

                p95_index = re.split("\s+", lines[6]).index("p95")
                qps_index = re.split("\s+", lines[6]).index("QPS")
                p95 = []
                qps = []
                for j in range(7, len(lines) - 11):
                    p95.append(float(lines[j].split()[p95_index])/1000.0)
                    qps.append(lines[j].split()[qps_index])

                file = open("../" + folder + "/" + str(i) + "/p95.csv", "w")
                file.write("time,p95,qps\n")
                time_count = ts_start
                index = 0
                print(complete_end_time - min_time)
                while time_count < ((complete_end_time - min_time) + step):
                    file.write(str(time_count if time_count > 0 else 0) + "," + str(p95[index]) + "," + str(qps[index])+ "\n")
                    time_count += step
                    index += 1

                file.close()
                    



