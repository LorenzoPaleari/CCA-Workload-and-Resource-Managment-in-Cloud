import os
import re

root_dir = './part_2a/'
regex = re.compile('^real.*\ds$')

for i in range(0, 7):
    values = []
    normalized = []
    parsec_bench = ""

    for name in sorted(os.listdir(root_dir)):
        if name != '.DS_Store':
            file_name = sorted(os.listdir(root_dir + name + "/"))[i]
            file = open(root_dir + name + "/" + file_name, "r")
            lines = file.readlines()
            parsec_bench = file_name[3:-4]

            value = 0.0
            for line in lines:
                if regex.match(line):
                    value += float(regex.match(line).group()[5:6]) * 60.0
                    value += float(regex.match(line).group()[7:-1])
                    break

            values.append(value)

    #print(values)
    normalized.append(1.00)
    for j in range(1, 7):
        normalized.append(round(values[j]/values[0], 2))

    print(parsec_bench + "\t" + str(normalized).replace(",", " &"))

