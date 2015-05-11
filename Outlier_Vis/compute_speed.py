import sys
import numpy as np
import csv
from datetime import datetime, timedelta
import dateutil.parser
import time
import os
import operator
from math import radians, cos, sin, asin, sqrt
#ID,NomePonto,Linha,Onibus,Hora,DiaMes,Mes,Ano,Velocidade,LatitudePonto,LongitudePonto,TimeStamp,DescricaoPonto

in_dir = "data_separated_by_line_and_day/"
files = [os.path.join(dp, f) for dp, _, filenames in os.walk(in_dir) for f in filenames]

def compute_speed(lat0, lon0, tmstp0, lat1, lon1, tmstp1):
  lon0, lat0, lon1, lat1 = map(radians, [lon0, lat0, lon1, lat1])
  dlon = lon1 - lon0 
  dlat = lat1 - lat0 
  a = sin(dlat/2)**2 + cos(lat0) * cos(lat1) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 
  kms = 6367. * c
  hours = (tmstp1 - tmstp0)/3600.
  return kms/hours
  

for in_file in files:
  if "sorted" in in_file:
    lst = open(in_file, 'r')
    lines = lst.readlines()[1:]
    lst.close()
    new_lines = ["ID,NomePonto,Linha,Onibus,Hora,DiaMes,Mes,Ano,Velocidade,LatitudePonto,LongitudePonto,TimeStamp,DescricaoPonto,Speed\n"]
    dic_data = {}
    for row in lines:
      speed = 0.0
      r = row.split(",")
      key = r[2]+'_'+r[3]+'_'+r[7]+'_'+r[6]+'_'+r[5]
      if key not in dic_data:        
        dic_data[key] = []
      dic_data[key].append(row)
    for k in dic_data.keys():
      csv_lines = dic_data[k]
      for ind, l in enumerate(csv_lines):
         try:
           l0 = csv_lines[ind].split(",")
           l1 = csv_lines[ind + 1].split(",")
           lat0, lon0, tmstp0, lat1, lon1, tmstp1 = l0[9], l0[10], time.mktime(dateutil.parser.parse(l0[11]).timetuple()), l1[9], l1[10], time.mktime(dateutil.parser.parse(l1[11]).timetuple())
           speed = compute_speed(float(lat0), float(lon0), float(tmstp0), float(lat1), float(lon1), float(tmstp1))
           new_lines.append(csv_lines[ind + 1].strip() + "," + str(speed) + "\n")  
         except:
           continue
    lst = open(in_file + "_with_speed", "w")
    for n in new_lines:
      lst.write(n)
    lst.close()
 
        
