import os
import re
import pandas as pd


def is_within_2500(val1, val2):
    return abs(val1 - val2) <= 2500


root_dir = '../part1/'

values = []
for k in range (1, 3):
    for l in range (1, 3):
        temp_values = []
        non_sorted_data = []
        values.append("Core_" + str(k) + "_Thread_" + str(l))

        #print(dir_name)
        for i in range(0, 3):
            file = open(root_dir + "results_core_" + str(k) + "_thread_" + str(l) + "_" + str(i) + ".txt", "r")
            lines = file.readlines()

            p95_index = re.split("\s+", lines[0]).index("p95")
            achieved_qps_index = re.split("\s+", lines[0]).index("QPS")
            for line in lines[1:-2]:
                numbers = re.split("\s+", line)
                temp_values.append([float(numbers[achieved_qps_index]), float(numbers[p95_index])/1000.0])

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

for i in range(0, 4):
    csv = open(root_dir + "/data_" + str(i) + ".csv", 'w')
    csv.write("x," + values[i * 2] + ",y_err_hi,y_err_lo,x_err\n")

    for data in values[i * 2 + 1]:
        csv.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "\n")

    csv.close()