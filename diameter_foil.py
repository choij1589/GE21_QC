import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from io import StringIO
import csv 
import numpy as np
import os

files = ['RO.csv', 'Drift.csv']

########edit case by case batch number, M type, directory path, and foil numbers
path_data = "../batch_09/Hole_Inspection/"
path_saved = "../batch_09/Result/Hole_Inspection/"
if not os.path.exists(path_saved):
    os.makedirs(path_saved)

batch_num = '09'
M_type = '2'

section = ['s1', 's2', 's3', 's4', 's5']

foil_A_num = ["19","20","21","22","24","25","26","28","29"]
foil_B_num = []
foil_num_list = foil_A_num + foil_B_num

for foil_num in foil_num_list:
    if foil_num in foil_A_num:
        text = "GE21-FOIL-M{}-G12-KR-B{}-00{}".format(M_type, batch_num, foil_num)
    else:
        text = "GE21-FOIL-M{}-G3-KR-B{}-00{}".format(M_type, batch_num, foil_num)

    dia_cu_mean, dia_cu_std, dia_pi_mean, dia_pi_std = [], [], [], []

    for i in range(len(files)):
        cu_mean, cu_std, pi_mean, pi_std = [], [], [], []
        with open(path_data+files[i], 'r') as raw:
            reader = csv.reader(raw)

            if 'Drift' in files[i]:
                val_range = [1, 2, 3, 4, 5]
            else:
                val_range = [4, 3, 2, 1, 5]

            for lines in reader:
                if foil_num + "_CUMean" in lines[0]:
                    cu_mean = [float(lines[i]) for i in val_range]
                elif foil_num + "_CUStdev" in lines[0]:
                    cu_std = [float(lines[i]) for i in val_range]
                elif foil_num + "_PIMean" in lines[0]:
                    pi_mean = [float(lines[i]) for i in val_range]
                elif foil_num + "_PIStdev" in lines[0]:
                    pi_std = [float(lines[i]) for i in val_range]

        dia_cu_mean.append(cu_mean)
        dia_cu_std.append(cu_std)
        dia_pi_mean.append(pi_mean)
        dia_pi_std.append(pi_std)

    fig, ax = plt.subplots()

    plt.errorbar(section, dia_cu_mean[0], yerr=dia_cu_std[0], marker="o", color="blue", capsize=3, label='RO Cu mean')
    plt.errorbar(section, dia_cu_mean[1], yerr=dia_cu_std[1], marker="o", color="red", capsize=3, label='Drift Cu mean')
    plt.errorbar(section, dia_pi_mean[0], yerr=dia_pi_std[0], marker="^", color="blue",capsize=3, label='RO PI mean', mfc='white')
    plt.errorbar(section, dia_pi_mean[1], yerr=dia_pi_std[1], marker="^", color="red", capsize=3, label='Drift PI mean', mfc='white')

    plt.xticks(section)
    plt.title(text)
    plt.xlabel("Section")
    plt.ylabel(r"Mean [$\mu$m]")
    plt.ylim(20, 90)

    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(path_saved+"F{}_diameter.png".format(foil_num))
