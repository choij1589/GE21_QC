import os
import ROOT
import glob
from array import array
import numpy as np
ROOT.gROOT.SetBatch(True)

##### Usage #####
"""python3 part1_tcv.py"""

# edit case by case batch number, M type, directory path, and foil number
path_data = ".data/M3_Batch_2/Part1/"
path_saved = ".results/M3_Batch_2/Part1/"
batch_num = "B03"
M_type = "M3"
#####

if not os.path.exists(path_saved+"Plots/"):
    os.makedirs(path_saved+"Plots/")
if not os.path.exists(path_saved+"ROOTs/"):
    os.makedirs(path_saved+"ROOTs/")
text_files = os.listdir(path_data)

for fname in text_files:
    print(fname)
    grid_num = fname.split("-")[3]
    foil_num = fname.split("-")[6][:4]
    text = f"GE21-FOIL-{M_type}-{grid_num}-KR-{batch_num}-{foil_num}"

    for txt in glob.glob(path_data+"/*.txt"):
        if fname in txt:
            # Some foil has data txt more than one
            if "test2" in txt or "2nd" in txt:
                data_num = "_2nd"
            elif "test3" in txt or "3rd" in txt:
                data_num = "_3rd"
            elif "Pre" in txt or "pre" in txt:
                data_num = "_Pre"
            else:
                data_num = ""

            with open(txt, "r") as f:
                data = f.readlines()
            outfile = ROOT.TFile.Open(
                path_saved+"/ROOTs/Part1_TCV_"+foil_num+data_num+".root", "RECREATE")
            time = array('f')
            voltage = array('f')
            current = array('f')

            for i in range(len(data)):
                ls = data[i].split()
                try:
                    val = float(ls[0])
                except ValueError:
                    continue
                time.append(float(ls[2]))
                voltage.append(float(ls[0]))
                current.append(float(ls[1]))

            #print(max(voltage), min(voltage))
            #print(max(current), min(current))
            #print(voltage)
            #print(current)
            clow = []
            chigh = []
            for v, c in zip(voltage, current):
                if len(str(c)) == 3 or str(c)[5:8] in ["000", "999"]:
                    continue
                else:
                    # Imon range high
                    if 95 < round(v) < 105:
                        clow.append(c)
                    elif 595 < round(v) < 605:
                        chigh.append(c)
                    else:
                        continue
            print(f"current diff.: {np.array(chigh).mean() - np.array(clow).mean()}")
            tg1 = ROOT.TGraph(len(time), time, voltage)
            tg1.SetTitle("; ;Voltage (V)")
            tg1.GetXaxis().SetLabelSize(0.05)
            tg1.GetXaxis().CenterTitle(1)
            tg1.GetYaxis().SetTitleOffset(0.6)
            tg1.GetYaxis().SetTitleSize(0.07)
            tg1.GetYaxis().SetLabelSize(0.05)
            tg1.GetYaxis().CenterTitle(1)
            tg1.SetMarkerStyle(20)
            tg1.SetMarkerSize(0.5)
            # tg1.SetMarkerStyle(ROOT.kFullDotMedium)
            tg1.SetMarkerColor(38)

            tg2 = ROOT.TGraph(len(time), time, current)
            tg2.SetTitle(";Time (s);Current (uA)")
            tg2.GetXaxis().SetLabelSize(0.05)
            tg2.GetYaxis().SetLabelSize(0.05)
            tg2.GetXaxis().SetTitleSize(0.06)
            tg2.GetXaxis().CenterTitle(1)
            tg2.GetYaxis().SetTitleSize(0.06)
            tg2.GetYaxis().CenterTitle(1)
            tg2.SetMarkerStyle(20)
            tg2.SetMarkerSize(0.5)
            # tg2.SetMarkerStyle(ROOT.kFullDotMedium)
            tg2.SetMarkerColor(ROOT.kRed)

            c = ROOT.TCanvas("c", "c")
            c.SetRightMargin(0.09)
            c.SetLeftMargin(0.12)
            c.SetBottomMargin(0.15)
            c.SetTopMargin(0.12)

            c.cd()
            tpad = ROOT.TPad("p1", "p1", 0.2, 0.2, 1, 1)
            tpad.SetFillStyle(4000)
            tpad.Draw()
            tpad.cd()
            title = ROOT.TLatex()
            title.DrawLatexNDC(.15, .95, text)

            c.SetGrid()
            c.Divide(1, 2, 0, 0)
            c.cd(1)
            c.cd(1).SetBottomMargin(0.05)
            tg1.Draw("AP")
            ROOT.gPad.SetGrid()

            c.cd(2)
            tg2.Draw("AP")
            ROOT.gPad.SetGrid()

            c.Write("Time-C+V")
            c.SaveAs(path_saved+"/Plots/Part1_TCV_"+foil_num+data_num+".png")
            c.Close()
            outfile.Write()
            outfile.Close()
