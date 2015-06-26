import os
import collections
import csv
import dateutil.parser
in_dir = "outliers/"
out_file_per_day = "number_of_outliers_per_day.csv"
out_file_per_day_hour_line = "number_of_outliers_per_day_hour_line.csv"
files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames]

dic_num_per_day = {}
dic_num_per_line = {}
dic_num_per_day_line_hour = {}
for in_file in files:
    day_month = in_file.replace(in_dir,"").replace(".csv", "")
    day, month = day_month.split("_")
    num_outliers = 0
    with open(in_file) as f:
        rows = csv.DictReader(f, delimiter=',')
        for row in rows:
            line = row["Linha"]
            timestamp = dateutil.parser.parse(row["TimeStamp_0"])
            hour = timestamp.hour
            year = timestamp.year
            key = str(year) + "," + str(month) + "," + str(day) + "," + str(hour) + "," + str(line)
            if key not in dic_num_per_day_line_hour:
                dic_num_per_day_line_hour[key] = 0
            dic_num_per_day_line_hour[key] += 1
            num_outliers += 1
        dic_num_per_day[100*int(month)+int(day)] = str(num_outliers) + "," + month + "/" + day +"\n"

#write the number of outliers per day
ordered = collections.OrderedDict(sorted(dic_num_per_day.items()))
fout = open(out_file_per_day, "wb")
fout.write("\"NumberOfOutliers\",\"Date\"\n")
for value in ordered.values():
    fout.write(value)
fout.close()

#write the number of outliers per day, hour and line
fout = open(out_file_per_day_hour_line, "wb")
fout.write("\"Year\",\"Month\",\"Day\",\"Hour\",\"Line\",\"NumberOfOutliers\"\n")
for key, value in dic_num_per_day_line_hour.items():
    fout.write(str(key) + "," + str(value)+"\n")
fout.close()
