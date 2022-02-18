import os,csv
import subprocess
import math
import pandas as pd

def sigma(l) :
  stdev=0 ; s = 0;
  avg = sum(l)/len(l)
  for n in l :
    s += (avg-n)*(avg-n)
  return math.sqrt(s/len(l))

pwd = os.getcwd()
d_sides = { "RO" : "Ro" , "D" : "Drift" }
# VER_BATCH_FOIL
dirs = [ name for name in os.listdir(pwd) if os.path.isdir(os.path.join(pwd, name)) and name != "results" ]
for d in dirs :
    foil = d.split("_")[2]
    foil_num = int(foil[0:4])

    if foil_num < 10 : 
      foil_str = f"0{str(foil_num)}"
    else : foil_str = str(foil_num)

    for side in d_sides.keys() :
      
      xlsx = pd.read_excel(f'{pwd}/{d}/{side}_Hole_Ins/{side}_Hole_Diameter_Inspection.xlsx', 'Sheet1', index_col=None)
      xlsx.to_csv(f'{pwd}/{d}/{side}_Hole_Ins/{side}_Hole_Diameter_Inspection.txt', sep='\t', encoding='utf-8',  index=False, line_terminator='\r\n')      

      raw_mean = subprocess.check_output(f"cat {pwd}/{d}/{side}_Hole_Ins/{side}_Hole_Diameter_Inspection.txt | grep Mean",shell=True).split(b"\r")
      raw_stddev = subprocess.check_output(f"cat {pwd}/{d}/{side}_Hole_Ins/{side}_Hole_Diameter_Inspection.txt | grep Std",shell=True).split(b"\r")

      mean = [ float(line.split(b"\t")[1].decode("utf-8")) for line in raw_mean if b'Mean' in line ]
      stddev = [ float(line.split(b"\t")[1].decode("utf-8")) for line in raw_stddev if b'Std' in line ]

      with open(f"{d_sides[side]}.csv",'a') as f_csv :
        write = csv.writer(f_csv)
        write.writerow([f"{foil_str}_CUMean"]+mean[0::2]+[sum(mean[0::2])/len(mean[0::2])])
        write.writerow([f"{foil_str}_CUStdev"]+stddev[0::2]+[sigma(stddev[0::2])])
        write.writerow([f"{foil_str}_PIMean"]+mean[1::2]+[sum(mean[1::2])/len(mean[1::2])])
        write.writerow([f"{foil_str}_PIStdev"]+stddev[1::2]+[sigma(stddev[1::2])])

#print(sigma([1.31,0.74,2.08,2.27,0.87]))



