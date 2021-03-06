import os
import collections
import csv
import dateutil.parser
in_dir = "outliers/"
out_file_per_day = "number_of_outliers_per_day.csv"
out_file_per_day_hour_line = "number_of_outliers_per_day_hour_line.csv"
out_file_per_day_hour_line_bus = "number_of_outliers_per_day_hour_line_bus.csv"
out_file_per_day_line = "number_of_outliers_per_day_line.csv"
files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames]

dic_num_per_day = {}
dic_num_per_day_line = {}
dic_num_per_day_line_hour = {}
dic_num_per_day_hour_line_bus = {}

for in_file in files:
    day_month = in_file.replace(in_dir,"").replace(".csv", "")
    day, month = day_month.split("_")
    num_outliers = 0
    with open(in_file) as f:
        rows = csv.DictReader(f, delimiter=',')
        for row in rows:
            line = row["Linha"] 
            busid = row["Onibus"]
            timestamp = dateutil.parser.parse(row["TimeStamp_0"])
            hour = timestamp.hour
            year = timestamp.year

            key = str(year) + "," + str(month) + "," + str(day) + "," + str(hour) + "," + str(line) + "," + str(busid)
            if key not in dic_num_per_day_hour_line_bus:
                dic_num_per_day_hour_line_bus[key] = 0
            dic_num_per_day_hour_line_bus[key] += 1

            key = str(year) + "," + str(month) + "," + str(day) + "," + str(hour) + "," + str(line)
            if key not in dic_num_per_day_line_hour:
                dic_num_per_day_line_hour[key] = 0
            dic_num_per_day_line_hour[key] += 1

            key2 = str(year) + "," + str(month) + "," + str(day) + "," + str(line)
            if key2 not in dic_num_per_day_line:
                dic_num_per_day_line[key2] = {}
            dic_num_per_day_line[key2][busid] = 0

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

#write the number of outliers per day and line
fout = open(out_file_per_day_line, "wb")
fout.write("\"Year\",\"Month\",\"Day\",\"Line\",\"NumberOfOutliers\"\n")
for key, value in dic_num_per_day_line.items():
    fout.write(str(key) + "," + str(len(value))+"\n")
fout.close()


#write the number of outliers per day, hour line and bus
fout = open(out_file_per_day_hour_line_bus, "wb")
fout.write("\"Year\",\"Month\",\"Day\",\"Hour\",\"Line\",\"BusId\",\"NumberOfOutliers\"\n")
for key, value in dic_num_per_day_hour_line_bus.items():
    fout.write(str(key) + "," + str(value)+"\n")
fout.close()

