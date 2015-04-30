import numpy as np
from datetime import datetime, timedelta
import dateutil.parser
import h5py
import csv
import os
DEBUG =1

stride = 10
time_size = 20

def create_hdf5(in_dir, out_dir):
    
    #load line definitions
    lines_dic = {}
    lines_lst = list(csv.reader(open('/home/rfn216/BusRio/lines_def.txt', 'rb'), delimiter=';'))
    for i,el in enumerate(lines_lst):
        lines_dic[el[0]] = i
    #add the null line
    lines_dic[""] = len(lines_lst)
    files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames if os.path.splitext(f)[1] == '.csv']
    #files = files[1:10]
    out_path_txt = out_dir+'/list_hdf5.txt'
    if os.path.exists(out_path_txt): os.remove(out_path_txt)
    lat_m, long_m = -22.9083, -43.1964#center of RJ coords
    day_m = 3600.*12.#mid_day in seconds
    for fp in files:
        data = list(csv.DictReader(open(fp, 'rb'), delimiter=';'))
        if data[0]['Linha'] in lines_dic: #only goes if the line is in the definition       
            data_size = len(data)
            if len(range(time_size,data_size,stride))>0:
                i=0
                data4D = np.zeros((len(range(time_size,data_size,stride)),3,1,time_size),dtype=np.float32)
                label2D = np.zeros((len(range(time_size,data_size,stride)),1),dtype=np.float32)
                for j in range(time_size,data_size,stride):
                    #print 'batch',j//stride,'of',data_size//stride
                    for k in range(time_size):
                        item = data[j-k]
                        timestamp = dateutil.parser.parse(item['TimeStamp']) #the start date starts at 0 minutes of the hour
                        data4D[i,0,0,k] = (float(item['LatitudePonto'])-lat_m)/0.1#/0.5 #divide by 0.1 in order to get larger numbers
                        data4D[i,1,0,k] = (float(item['LongitudePonto'])-long_m)/0.1#/0.5  #divide by 0.1 in order to get larger numbers
                        data4D[i,2,0,k] = ((timestamp.hour*3600+timestamp.minute*60+timestamp.second)-day_m)/(2*day_m) #subtract mean sec day and divide by day total seconds. This normalization between [-0.5,0.5]
                    
                    label2D[i,0] = lines_dic[item['Linha']] #Get only the last ground_truth
                        
                    i=i+1
                #save as hdf5
                with h5py.File(out_dir+fp.replace(in_dir,'').replace('.csv','.h5'), 'w') as f:
                    f.create_dataset('data', data=data4D, compression="gzip")
                    f.create_dataset('label', data=label2D)
                with open(out_path_txt, 'a') as f:
                    f.write(out_dir+fp.replace(in_dir,'').replace('.csv','.h5')+'\n')
        else:
            #print 'line not found:',data[0]['Linha']  
            pass

train_in_dir = '/work/rfn216/bus_rio/split_with_null_5/'
train_out_dir = '/work/rfn216/bus_rio/hdf5_with_null_5/'

create_hdf5(train_in_dir, train_out_dir)
