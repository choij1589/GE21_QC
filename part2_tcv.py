import os
import argparse
import ROOT
import glob
import numpy as np
from array import array
ROOT.gROOT.SetBatch(True)

# example usgae
"""python3 part2_tcv.py -c 2 3 4 5 6 -f 13A 16A 8B 20A 6B"""

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--channels", "-c", nargs="+", default=None,
                    required=True, type=int, help="HV channels")
parser.add_argument("--foils", "-f", nargs="+", default=None,
                    required=True, type=str, help="corresponding foil numbers")
args = parser.parse_args()

# edit case by case batch number, M type, directory path, foil number, channel number, and file name
path_data = ".data/M3_Batch_3/QC2_Long_Data/Part2"
path_saved = ".results/M3_Batch_3/Part2/"
batch_num = "B03"
M_type = "M3"
#####

if not os.path.exists(path_saved+"Plots/"):
    os.makedirs(path_saved+"Plots/")
if not os.path.exists(path_saved+"ROOTs/"):
    os.makedirs(path_saved+"ROOTs/")

# match channels and foils
channels = args.channels
foils = args.foils
assert len(channels) == len(foils)
print(f"HV channels:\t{channels}")
print(f"cor. foils:\t{foils}")

fname = ""
for (ch, f) in zip(channels, foils):
    fname += f"Ch{ch}F{f[:-1]}_"
fname = fname[:-1]
print(f"input text name: {fname}")

foil_A_num = []
foil_B_num = []
foil_A_channel = []
foil_B_channel = []
for (ch, f) in zip(channels, foils):
    foil_num = "0"*(5-len(f)) + f[:-1]
    if "A" in f:
        foil_A_num.append(foil_num)
        foil_A_channel.append(ch)
    elif "B" in f:
        foil_B_num.append(foil_num)
        foil_B_channel.append(ch)
    else:
        print(f"[Error] Wrong foil number {f}")
        raise ValueError

foil_num_list = foil_A_num + foil_B_num
foil_channel_list = foil_A_channel + foil_B_channel

for fn, foil_num in enumerate(foil_num_list):
    if foil_num in foil_A_num:
        text = "GE21-FOIL-{}-G12-KR-{}-{}".format(M_type, batch_num, foil_num)
    else:
        text = "GE21-FOIL-{}-G3-KR-{}-{}".format(M_type, batch_num, foil_num)

    txtlists = glob.glob(path_data+"/*.txt")
    for txt in txtlists:
        print(txt)
        if fname in txt:
            if "test2" in txt or "2nd" in txt:
                data_num = "_2nd"
            elif "test3" in txt or "3rd" in txt:
                data_num = "_3rd"
            elif "Pre" in txt or "pre" in txt:
                data_num = "_Pre"
            else:
                data_num = ""  # Some foil has data txt more than one ex) 1st, 2nd or test1, test2 or Pre

            with open(txt, "r") as f:
                data = f.readlines()

            outfile = ROOT.TFile.Open(
                path_saved+"/ROOTs/Part2_TCV_"+foil_num+data_num+".root", "RECREATE")

            time = array('f')
            voltage = array('f')
            current = array('f')
            for i in range(len(data)):
                ls = data[i].split()
                try:
                    val = float(ls[0])
                except ValueError:
                    continue
                time.append(float(ls[0]))
                voltage.append(float(ls[foil_channel_list[fn]+1]))
                current.append(float(ls[foil_channel_list[fn]+9]))

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
            c.SaveAs(path_saved+"Plots/Part2_TCV_"+foil_num+data_num+".png")
            c.Close()
            outfile.Write()
            outfile.Close()
