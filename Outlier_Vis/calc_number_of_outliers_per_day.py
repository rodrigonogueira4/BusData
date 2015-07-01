import os
import collections
in_dir = "outliers/"
out_file = "number_of_outliers_per_day.csv"
files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames]

dic_out = {}
for in_file in files:
    day_month = in_file.replace(in_dir,"").replace(".csv", "")
    day, month = day_month.split("_")
    num_lines = sum(1 for line in open(in_file))
    dic_out[100*int(month)+int(day)] = str(num_lines-1) + "," + month + "/" + day +"\n"


ordered = collections.OrderedDict(sorted(dic_out.items()))

fout = open(out_file, "wb")
fout.write("\"NumberOfOutliers\",\"Date\"\n")
for value in ordered.values():
    fout.write(value)
fout.close()
