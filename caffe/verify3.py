import sys
caffe_root = '/opt/caffe/'  # this file is expected to be in {caffe_root}/examples
sys.path.insert(0, caffe_root + 'python')
import numpy as np
import caffe
import csv
from datetime import datetime, timedelta
import dateutil.parser
import os

DEBUG =0
stride = 10
time_size = 20
min_acc = 0.1 #min accuracy to be considered outlier
in_dir = '/work/rfn216/bus_rio/raw_1/'
#outputfile = 'output_7_jan.csv'
#day = 07 #it can be day = None
#month = 01 #it can be month = None

day = int(sys.argv[1])
month = int(sys.argv[2])

print "day", day
print "month",month
outputfile = "/work/rfn216/bus_rio/outliers1/" + str(day) + "_" + str(month) + ".csv"

#load line definitions
lines_dic = {}
lines_lst_inv = []
for i,el in enumerate(list(csv.reader(open('/home/rfn216/BusRio/lines_def.txt', 'rb'), delimiter=';'))):
    lines_dic[el[0]] = i
    lines_lst_inv.append(el[0])

lat_m, long_m = -22.9083, -43.1964#center of RJ coords
day_m = 3600.*12.#mid_day in seconds
net = caffe.Classifier('/home/rfn216/BusRio/deploy7.prototxt', '/work/rfn216/bus_rio/busrio7_iter_2000000.caffemodel')
net.set_phase_test()
net.set_mode_gpu()
y_pred =[]
out_data = []
dic_data={}
print "day", day
print "month",month
out = csv.writer(open(outputfile, 'wb'))
files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames]

for in_file in files:
	lst = csv.DictReader(open(in_file,'r'), delimiter=',')

	for row in lst:

		if row['Linha'] not in lines_dic: #only goes if the line is in the definition
		    #print 'Line not in line definition file:',row['Linha']
		    continue

		if day !=None and month !=None:
			if day != int(row['DiaMes']) or month != int(row['Mes']):
				continue

		key = row['Linha']+'_'+row['Onibus']+'_'+row['Ano']+'_'+row['Mes']+'_'+row['DiaMes']
		if key not in dic_data:        
		    dic_data[key] = []
		dic_data[key].append(row)

#order by timestamp
for key in dic_data.keys():
    ts = []
    for item in dic_data[key]:
        ts.append(dateutil.parser.parse(item['TimeStamp']))
    idx_sorted = np.asarray(ts).argsort()
    dic_data[key] = dic_data[key][idx_sorted]

#i =0
header=False
for key, rows in dic_data.items():
    #i=i+1    
    #if i>1000:
    #    break        
   
    data_size = len(rows)
    if len(range(time_size,data_size,stride))>0:
        for j in range(time_size,data_size,stride):
            data4D = np.zeros((1,3,1,time_size),dtype=np.float32)
            for k in range(time_size):
                item = rows[j-k]
                timestamp = dateutil.parser.parse(item['TimeStamp'])
                rows[0]['TimeStamp_'+str(k)] = timestamp
                rows[0]['LatitudePonto_'+str(k)] = item['LatitudePonto']
                rows[0]['LongitudePonto_'+str(k)] = item['LongitudePonto']
                data4D[0,0,0,k] = (float(item['LatitudePonto'])-lat_m)/0.1#/0.5 #divide by 0.1 in order to get larger numbers
                data4D[0,1,0,k] = (float(item['LongitudePonto'])-long_m)/0.1#/0.5  #divide by 0.1 in order to get larger numbers
                data4D[0,2,0,k] = ((timestamp.hour*3600+timestamp.minute*60+timestamp.second)-day_m)/(2*day_m) #subtract mean sec day and divide by day total seconds.
            scores = net.forward(data=data4D)['prob'][0,:,0,0]
            idx = scores.argmax()
            pred = lines_lst_inv[idx]
            accu = scores[idx]
            if DEBUG>=1: 
                print 'row:', rows[0],' line ground:', rows[0]['Linha'],' line pred:',pred 
            rows[0]['Linhapred'] = pred
            rows[0]['LinhaAccu'] = accu
            
            if not header:
                out.writerow(rows[0].keys())
                header = True
            if accu < min_acc: #only write if the accuracy is lower than a certain threshold
                out.writerow(rows[0].values())


