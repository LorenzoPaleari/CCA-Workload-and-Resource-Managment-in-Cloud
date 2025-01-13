import os
import re

root_dir = './part2b/'
data = root_dir + 'data.csv'
regex = re.compile('^real.*\ds$')

values = []
normalized = []
for i in range(0, 7):
    parsec_bench = ""

    for name in sorted(os.listdir(root_dir)):
        if name != '.DS_Store' and name != "data.csv":
            file_name = sorted(os.listdir(root_dir + name + "/"))[i]
            file = open(root_dir + name + "/" + file_name, "r")
            lines = file.readlines()
            parsec_bench = file_name[3:-4]
            #print(file_name)
            #print(name)

            value = 0.0
            for line in lines:
                if regex.match(line):
                    print(regex.match(line))
                    value += float(regex.match(line).group()[5:6]) * 60.0
                    value += float(regex.match(line).group()[7:-1])
                    break

            values.append(value)

    normalized.append(parsec_bench)
    normalized.append(1.0)
    for j in range(1, 4):
        normalized.append(round(values[0 + i*4]/values[j + i*4], 2))

#print(values)
#print(normalized)

csv = open(data, 'w')
row = ""
for i in range(0, 5):
    if i == 0:
        row = "x,"
    else:
        row = "" + str(int(i/3) + int(i/4)*3 + i) + ","

    for j in range(i, len(normalized), 5):
        row += str(normalized[j]) + ","

    csv.write(row[:-1] + "\n")

csv.close()

