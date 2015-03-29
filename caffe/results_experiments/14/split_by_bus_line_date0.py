import csv
import os.path

in_dir = '/work/rfn216/bus_rio/raw_0/'
output_dir = '/work/rfn216/bus_rio/split_0/'
#data_rows = csv.reader(open(data_file_path, 'rb'), delimiter=',')

files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames]

for fp in files:
	data_rows = csv.DictReader(open(fp, 'rb'), delimiter=',')

	for row in data_rows:
	    if row['Linha']!='':
	    #if row[2]!='':
		out_file_name = row['Linha']+'_'+row['Onibus']+'_'+row['Ano']+'_'+row['Mes']+'_'+row['DiaMes']+'.csv'
		#out_file_name = row[2]+'_'+row[3]+'_'+row[7]+'_'+row[6]+'_'+row[5]+'.csv'
		
		write_header=False
		if not os.path.isfile(output_dir+'/'+out_file_name): #write headers if file does not exists
		    write_header=True
		    
		with open(output_dir+'/'+out_file_name,'a') as f:
		    csvfile = csv.writer(f, delimiter=';', lineterminator='\n')
		    if write_header:
		        csvfile.writerow(row.keys())
		    csvfile.writerow(row.values())
		    #csvfile.writerow(row)
            
print 'finished'
