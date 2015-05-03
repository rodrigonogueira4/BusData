import sys
import numpy as np
import csv
from datetime import datetime, timedelta
import dateutil.parser
import time
import os
import operator

#ID,NomePonto,Linha,Onibus,Hora,DiaMes,Mes,Ano,Velocidade,LatitudePonto,LongitudePonto,TimeStamp,DescricaoPonto

in_dir = "data_separated_by_line_and_day/"
files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames]


for in_file in files:
        #print in_file
        dic_data = {}
	lst = open(in_file, 'r')
        lines = lst.readlines()
        lines = lines[2:]
        lst.close()
	csv_lines = ["ID,NomePonto,Linha,Onibus,Hora,DiaMes,Mes,Ano,Velocidade,LatitudePonto,LongitudePonto,TimeStamp,DescricaoPonto\n"]        
        try:
          for row in lines:
            r = row.split(",")
            key = r[2]+'_'+r[3]+'_'+r[7]+'_'+r[6]+'_'+r[5]
	    if key not in dic_data:        
               dic_data[key] = []
	    dic_data[key].append(row)
	  
          for key in dic_data.keys():
            ts = {}
            for item in dic_data[key]:
              i = item.split(",")
              t1 = dateutil.parser.parse(i[11]).timetuple()
              ts[item] = time.mktime(t1)
	    idx_sorted = sorted(ts.items(), key=operator.itemgetter(1))
	    for idx in idx_sorted:
              csv_lines.append(idx[0])
        except:
          continue

        lst2 = open(in_file + "_sorted", 'w+')
        for l in csv_lines:
          lst2.write(l)
        lst2.close()
