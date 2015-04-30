import csv
import os.path
import dateutil.parser
from datetime import datetime, timedelta

input_dir = 'C:/NYU/BusRio/Splitted_Data/'
output_dir = 'C:/NYU/BusRio/Fitted_Data/'
#utc=pytz.UTC

infiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_dir) for f in filenames if os.path.splitext(f)[1] == '.csv']
for fpath in infiles:
    print 'processing',fpath
    data_rows = csv.reader(open(fpath, 'rb'), delimiter=';')
    last_row = data_rows.next()#get the first row
    
    first_time = dateutil.parser.parse(last_row[4]).replace(minute=0,second=0) #the start date starts at 0 minutes of the hour
    
    for add_min in range(0,(24-first_time.hour)*60,5):
        curr_ref_time = first_time + timedelta(minutes=add_min)
        
        stop = False
        last_row_time = dateutil.parser.parse(last_row[4])
        if last_row_time < curr_ref_time:
            curr_row = next(data_rows,None)
            if curr_row ==None:
                break
            last_row = curr_row
            while True: #search until the date is greater
                
                curr_row_time = dateutil.parser.parse(curr_row[4]) 
                if curr_row_time > curr_ref_time:
                    break
                curr_row = next(data_rows,None)
                if curr_row ==None:
                    stop = True
                    break
                    
        if stop:
            break
        output_row = list(last_row)
        output_row[4] =str(curr_ref_time) 
        #write line to the output file with the modified timestamp
        with open(output_dir+'/'+fpath.replace(input_dir,''),'a') as f:
            csvfile = csv.writer(f, delimiter=';', lineterminator='\n')
            csvfile.writerow(output_row)
print 'finished'