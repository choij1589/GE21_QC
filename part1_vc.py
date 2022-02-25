import os
from re import I
import ROOT
import matplotlib.pyplot as plt
import numpy as np

##### Usage #####
"""python3 part1_vc.py"""

# edit case by case batch number, M type, directory path, and foil number
path_data = ".data/M3_Batch_3/QC2_Long_Data/Part1/"
path_saved = ".results/M3_Batch_3/Part1/"
batch_num = "B03"
M_type = "M3"

#####
if not os.path.exists(path_saved+"Plots/"):
    os.makedirs(path_saved+"Plots/")
if not os.path.exists(path_saved+"ROOTs/"):
    os.makedirs(path_saved+"ROOTs/")

text_files = os.listdir(path_data)
for fname in text_files:
    print("Processing "+fname)
    print(fname)
    grid_num = fname.split("-")[3]
    foil_num = fname.split("-")[6][:4]
    #foil_num = fname[40]+fname[41]
    text = f"GE21-FOIL-{M_type}-{grid_num}-KR-{batch_num}-{foil_num}"

    with open(path_data+fname, "r") as f:
        data = f.readlines()
    print("file for foil %s open success" % foil_num)
    if "1st" in fname:
        outfile = ROOT.TFile.Open(
            path_saved+"/ROOTs/Part1_VC_"+foil_num+".root", "RECREATE")
    if "2nd" in fname:
        outfile = ROOT.TFile.Open(
            path_saved+"/ROOTs/Part1_VC_"+foil_num+"_2nd.root", "RECREATE")
    if "3rd" in fname:
        outfile = ROOT.TFile.Open(
            path_saved+"/ROOTs/Part1_VC_"+foil_num+"_3rd.root", "RECREATE")
    if "4th" in fname:
        outfile = ROOT.TFile.Open(
            path_saved+"/ROOTs/Part1_VC_"+foil_num+"_4th.root", "RECREATE")
    else:
        outfile = ROOT.TFile.Open(
            path_saved+"/ROOTs/Part1_VC_"+foil_num+".root", "RECREATE")
    currents = [[] for i in range(11)]
    t, v, c, prev = 0, 0, 0, False
    for line in data:

        ls = line.split("\t")
        try:
            val = float(ls[0])
        except ValueError:
            continue
        except ZeroDivisionError:
            continue

        t, v, c = float(ls[2]), float(ls[0]), float(ls[1])
        vi = int(round(v / 50))
        if (vi < 2 or abs(v-vi*50) > 1):
            continue
        if (c*1e6) % 1000 == 0 and t > 500:
            break  # We only need early data when voltages rises until 600V
        if c == 0:
            prev = False
            continue
        if (c*1e6) % 1000 != 0:  # Current resolution should be 50pA, not 1nA
            if 1000*c < 9:
                # Ignoring the effect of Spark (I < 9nA)
                currents[vi-2].append(1000*c)
            # else: print("Spark during good resolution at t,c = %f, %f"%(t,c))
            prev = True
        # But in some rare cases, current can be multiples of 1000pA(=1nA)
        elif (c*1e6) % 1000 == 0 and prev:
            if 1000*c < 9:
                # Ignoring the effect of Spark (I < 9nA)
                currents[vi-2].append(1000*c)

    currents.pop(1)
    currents = np.array(currents, dtype=object)
    voltage = np.array([100, 200, 250, 300, 350, 400, 450, 500, 550, 600])
    mean = [np.mean(c) for c in currents]
    std = [np.std(c) for c in currents]
    print("Foil Number :", foil_num, ", Currents(nA) of (600V, 100V, Diff) : (%.3f, %.3f, %.3f)" % (
        mean[9], mean[0], mean[9] - mean[0]))

    MEDIUM_SIZE = 12
    BIGGER_SIZE = 14

    plt.rc('font', size=MEDIUM_SIZE)
    plt.rc('axes', labelsize=BIGGER_SIZE)

    plt.errorbar(voltage, mean, std, marker='*', linestyle="none")
    plt.title(text)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (nA)")
    plt.tight_layout()

    if "1st" in fname:
        plt.savefig(path_saved+"/Plots/Part1_VC_{}.png".format(foil_num))
    if "2nd" in fname:
        plt.savefig(path_saved+"/Plots/Part1_VC_{}_2nd.png".format(foil_num))
    if "3rd" in fname:
        plt.savefig(path_saved+"/Plots/Part1_VC_{}_3rd.png".format(foil_num))
    if "4th" in fname:
        plt.savefig(path_saved+"/Plots/Part1_VC_{}_4th.png".format(foil_num))
    else:
        plt.savefig(path_saved+"/Plots/Part1_VC_{}.png".format(foil_num))
    plt.clf()
