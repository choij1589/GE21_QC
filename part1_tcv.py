import ROOT, os, glob
import numpy as np
from array import array
ROOT.gROOT.SetBatch(True)

########edit case by case batch number, M type, directory path, and foil number
# Open file
path_data = "../batch_09/QC2Long1/"
path_saved = "../batch_09/Result/QC2Long_part1/" 
if not os.path.exists(path_saved+"Plots/"): os.makedirs(path_saved+"Plots/")
if not os.path.exists(path_saved+"ROOTs/"): os.makedirs(path_saved+"ROOTs/")

batch_num = '09'
M_type = '2'

foil_A_num = ["22","26"]
foil_B_num = []
foil_num_list = foil_A_num + foil_B_num

for foil_num in foil_num_list:
    if foil_num in foil_A_num:
        fname = "QC2LONG_PART1_GE21-FOIL-M{}-G12-KR-B{}-00{}".format(M_type, batch_num, foil_num)
        text = "GE21-FOIL-M{}-G12-KR-B{}-00{}".format(M_type, batch_num, foil_num)
    else:
        fname = "QC2LONG_PART1_GE21-FOIL-M{}-G3-KR-B{}-00{}".format(M_type, batch_num, foil_num)
        text = "GE21-FOIL-M{}-G3-KR-B{}-00{}".format(M_type, batch_num, foil_num)

    txtlists = glob.glob(path_data+"/*.txt")
    for txt in txtlists:
        if fname in txt:
            if "test2" in txt or "2nd" in txt:
                data_num = "_2nd"
            elif "test3" in txt or "3rd" in txt:
                data_num = "_3rd"
            elif "Pre" in txt or "pre" in txt:
                data_num = "_Pre"
            else:
                data_num = "" # Some foil has data txt more than one ex) 1st, 2nd or test1, test2 or Pre

            with open(txt, "r") as f:
                data = f.readlines()

            outfile = ROOT.TFile.Open(path_saved+"/ROOTs/Part1_TCV_"+foil_num+data_num+".root", "RECREATE")
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

            print(max(voltage))
            print(max(current))

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
            #tg1.SetMarkerStyle(ROOT.kFullDotMedium)
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
            #tg2.SetMarkerStyle(ROOT.kFullDotMedium)
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
