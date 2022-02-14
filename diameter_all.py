import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from io import StringIO
import csv 
import os

foil_num = []
dia_cu_mean, dia_cu_std, dia_pi_mean, dia_pi_std = [], [], [], []

files = ['RO.csv', 'Drift.csv']

########edit case by case batch number, M type, and directory path
path_data = "../batch_09/Hole_Inspection/"
path_saved = "../batch_09/Result/Hole_Inspection/"
if not os.path.exists(path_saved):
    os.makedirs(path_saved)

batch_num = '09'
M_type = '2'

for file_idx in range(len(files)):
    cu_mean, cu_std, pi_mean, pi_std = [], [], [], []
    with open(path_data + files[file_idx], 'r') as raw: 
        reader = csv.reader(raw)
        print("File : ", files[file_idx])
        for lines in reader: 
            xs = lines[0][0:2]

            if "CUMean" in lines[0]:
                if "RO" in files[file_idx]:
                    foil_num.append(xs)
                cu_mean.append(float(lines[6]))
            elif "CUStdev" in lines[0]:
                cu_std.append(float(lines[6]))
            elif "PIMean" in lines[0]:
                pi_mean.append(float(lines[6]))
            elif "PIStdev" in lines[0]:
                pi_std.append(float(lines[6]))
            else: continue
    dia_cu_mean.append(cu_mean)
    dia_cu_std.append(cu_std)
    dia_pi_mean.append(pi_mean)
    dia_pi_std.append(pi_std)

fig, ax = plt.subplots()

plt.errorbar(foil_num, dia_cu_mean[0], yerr=dia_cu_std[0], marker="o", color="blue", capsize=3, label='RO Cu mean')
plt.errorbar(foil_num, dia_cu_mean[1], yerr=dia_cu_std[1], marker="o", color="red", capsize=3, label='Drift Cu mean')
plt.errorbar(foil_num, dia_pi_mean[0], yerr=dia_pi_std[0], marker="^", color="blue",capsize=3, label='RO PI mean', mfc='white')
plt.errorbar(foil_num, dia_pi_mean[1], yerr=dia_pi_std[1], marker="^", color="red", capsize=3, label='Drift PI mean', mfc='white')
plt.title("Hole Diameter Inspection")
plt.xlabel("Foil Number")
plt.ylabel(r"Mean [$\mu$m]")
plt.ylim(20, 90)
plt.xticks(rotation=45)

info = 'Foil Type: M{} \nBatch Number: {} \nProduction Site: KR'.format(M_type, batch_num)
props = dict(boxstyle='round', alpha=0.5, ec='gray', fc='white')
plt.text(0, 26, info, bbox=props) 
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig(path_saved+"diameter.png")
#plt.show()
