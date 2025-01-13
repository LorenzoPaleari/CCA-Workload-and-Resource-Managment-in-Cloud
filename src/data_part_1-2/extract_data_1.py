import os
import re
import pandas as pd


def is_within_2500(val1, val2):
    return abs(val1 - val2) <= 2500


root_dir = './part_1/'

values = []
for dir_name in sorted(os.listdir(root_dir)):
    if re.search('^data', dir_name) is None:
        temp_values = []
        non_sorted_data = []
        values.append(dir_name[10:])

        #print(dir_name)
        for i in range(1, 18):
            for file_name in sorted(os.listdir(root_dir + dir_name)):
                file = open(root_dir + dir_name + "/" + file_name, "r")
                lines = file.readlines()

                numbers = re.split("\s+", lines[i])
                #print(numbers)
                temp_values.append([float(numbers[16]), float(numbers[12])])

        temp_values = sorted(temp_values, key=lambda x: x[0])

        qps = [temp_values[0][0]]
        p95 = [temp_values[0][1]]
        actual = round(qps[0]/5000) * 5000
        for i in range(1, len(temp_values)):
            if is_within_2500(temp_values[i][0], actual):
                qps.append(temp_values[i][0])
                p95.append(temp_values[i][1])
            else:
                non_sorted_data.append([pd.Series(qps).mean(), pd.Series(p95).mean(), pd.Series(p95).max() - pd.Series(p95).mean(), pd.Series(p95).mean() - pd.Series(p95).min(), pd.Series(qps).std()])
                qps = [temp_values[i][0]]
                p95 = [temp_values[i][1]]
                actual = round(qps[0] / 5000) * 5000
        non_sorted_data.append(
            [pd.Series(qps).mean(), pd.Series(p95).mean(), pd.Series(p95).max() - pd.Series(p95).mean(), pd.Series(p95).mean() - pd.Series(p95).min(), pd.Series(qps).std()])
        values.append(sorted(non_sorted_data, key=lambda x: x[0]))

for i in range(0, 7):
    csv = open(root_dir + "/data_" + str(i) + ".csv", 'w')
    csv.write("x," + values[i * 2] + ",y_err_hi,y_err_lo,x_err\n")

    for data in values[i * 2 + 1]:
        csv.write(str(data[0]) + "," + str(data[1] / 1000.0) + "," + str(data[2] / 1000.0) + "," + str(data[3] / 1000.0) + "," + str(data[4]) + "\n")

    csv.close()
