import ROOT, glob, os
import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime

########edit case by case batch number, M type, directory path, and foil number
path_data = "../batch_09/QC2Long1/"
path_saved = "../batch_09/Result/QC2Long_part1/"

if not os.path.exists(path_saved+"Plots/"): os.makedirs(path_saved+"Plots/")
if not os.path.exists(path_saved+"ROOTs/"): os.makedirs(path_saved+"ROOTs/")
batch_num = '09'
M_type = '2'

foil_A_num = ["22","26"]
foil_B_num = []
foil_num_list = foil_A_num + foil_B_num
dir_list = os.listdir(path_data)
print(dir_list)
for fname in dir_list:
    print("Processing "+fname)
    foil_num = fname[40]+fname[41]
    text = "GE21-FOIL-M{}-G12-KR-B{}-00{}".format(M_type, batch_num, foil_num)


    with open(path_data+fname, "r") as f: data = f.readlines()
    print("file for foil %s open success" %foil_num)
    if "1st" in fname:
        outfile = ROOT.TFile.Open(path_saved+"/ROOTs/Part1_VC_"+foil_num+".root", "RECREATE")
    if "2nd" in fname:
        outfile = ROOT.TFile.Open(path_saved+"/ROOTs/Part1_VC_"+foil_num+"_2nd.root", "RECREATE")
    if "3rd" in fname:
        outfile = ROOT.TFile.Open(path_saved+"/ROOTs/Part1_VC_"+foil_num+"_3rd.root", "RECREATE")
    if "4th" in fname:
        outfile = ROOT.TFile.Open(path_saved+"/ROOTs/Part1_VC_"+foil_num+"_4th.root", "RECREATE")
    else:
        outfile = ROOT.TFile.Open(path_saved+"/ROOTs/Part1_VC_"+foil_num+".root", "RECREATE")
    currents = [[] for i in range(11)]
    t, v, c, prev = 0, 0, 0, False
    for line in data:

        ls=line.split("\t")
        try: val = float(ls[0])
        except ValueError: continue
        except ZeroDivisionError: continue

        t, v, c = float(ls[2]), float(ls[0]), float(ls[1])
        vi = int(round(v / 50))
        if (vi < 2 or abs(v-vi*50)>1): continue
        if (c*1e6)%1000 == 0 and t > 500: break # We only need early data when voltages rises until 600V
        if c==0:
            prev = False
            continue
        if (c*1e6)%1000 != 0: # Current resolution should be 50pA, not 1nA
            if 1000*c < 9: currents[vi-2].append(1000*c) # Ignoring the effect of Spark (I < 9nA)
            #else: print("Spark during good resolution at t,c = %f, %f"%(t,c))
            prev = True
        elif (c*1e6)%1000 == 0 and prev: # But in some rare cases, current can be multiples of 1000pA(=1nA)
            if 1000*c < 9: currents[vi-2].append(1000*c) # Ignoring the effect of Spark (I < 9nA)

    currents.pop(1)
    currents = np.array(currents, dtype=object)
    voltage = np.array([100, 200, 250, 300, 350, 400, 450, 500, 550, 600])
    mean = [np.mean(c) for c in currents]
    std = [np.std(c) for c in currents]
    print("Foil Number :",foil_num,", Currents(nA) of (600V, 100V, Diff) : (%.3f, %.3f, %.3f)"%( mean[9], mean[0], mean[9] - mean[0]))

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
