import csv

dic = {} 
data_rows = csv.reader(open("/home/rfn/NYU/BusRio/data_all.csv", 'rb'), delimiter=';')


for row in data_rows:

    dic[row[3]] = True
print dic.keys()
print len(dic.keys())