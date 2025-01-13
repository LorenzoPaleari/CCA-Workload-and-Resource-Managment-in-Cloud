import os
from datetime import datetime

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
                
                for line in lines:
                    if any(word in line[1] for word in ["start", "end", "pause", "unpause"]) and "scheduler" not in line[2]:
                        if "start" in line[1]:
                            times[line[2]] = [line[0] - min_time]
                        else:
                            times[line[2]].append(line[0] - min_time)

                print("\n\n" + folder + "/" + str(i) + "/" + file_name)
                for key in times:
                    print("Job: " + key)
                    
                    sum = 0
                    for j in range(0, len(times[key]), 2):
                        sum += times[key][j + 1] - times[key][j]
                    print("Total time: " + str(sum) + "\n")

                print("Total time: " + str(max_time - min_time) + "\n\n")



