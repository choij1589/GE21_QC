import os
from math import isnan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Usage
"""python3 hole_inspection.py"""

##### edit case by case #####
path_data = ".data/M3_Batch_2"
path_saved = ".results/M3_Batch_2/Hole_Diameters"
M_type = 3
batch_num = "02"
#####

if not os.path.exists(path_saved):
    os.makedirs(path_saved)

##### read directories #####
dirs = os.listdir(path_data)

##### helper functions #####


def read_data(excel):
    inspections = {
        "s1_Cu": [],
        "s1_PI": [],
        "s2_Cu": [],
        "s2_PI": [],
        "s3_Cu": [],
        "s3_PI": [],
        "s4_Cu": [],
        "s4_PI": [],
        "s5_Cu": [],
        "s5_PI": []
    }

    keys = list(inspections.keys())
    k_iter = iter(keys)
    for idx in excel.index:
        label, value = excel.iloc[idx, 0], excel.iloc[idx, 1]
        #print(df.iloc[idx, 0], type(df.iloc[idx, 0]), df.iloc[idx, 1], type(df.iloc[idx, 1]))
        if type(label) == str and label == "Obj #" and value == "Diameter":
            key = next(k_iter)
        elif type(label) != str and not isnan(label) and not isnan(value):
            inspections[key].append(value)
        elif type(label) == str:
            is_summary = True
        elif isnan(label):
            is_blank = True
        else:
            print(excel.iloc[idx, 0], excel.iloc[idx, 1])

    return inspections


def analyze(inspections):
    # return means and stds for each section
    Cu_means = []
    Cu_stds = []
    PI_means = []
    PI_stds = []

    for key in inspections.keys():
        if "Cu" in key:
            Cu = np.array(inspections[key])
            Cu_means.append(round(Cu.mean(), 2))
            Cu_stds.append(round(Cu.std(), 2))
        elif "PI" in key:
            PI = np.array(inspections[key])
            PI_means.append(round(PI.mean(), 2))
            PI_stds.append(round(PI.std(), 2))

    return Cu_means, Cu_stds, PI_means, PI_stds


def deco(total_ins):
    df = pd.DataFrame(data=total_ins).transpose()
    df.set_axis(['1', '2', '3', '4', '5'], axis=1, inplace=True)

    CU = df.copy()
    for idx in CU.index:
        if "PI" in idx:
            CU.drop(labels=idx, inplace=True)
    CU["tmp_idx"] = 0.
    CU["index"] = CU.index
    CU["Mean"] = 0.
    for i, idx in enumerate(CU.index):
        if "Mean" in idx:
            CU.loc[idx, "tmp_idx"] = int(idx.split("_")[0])+0.1
            CU.loc[idx, "Mean"] = round(CU.iloc[i, :5].mean(), 2)
        elif "Stdev" in idx:
            CU.loc[idx, "tmp_idx"] = int(idx.split("_")[0])+0.2
            CU.loc[idx, "Mean"] = round(CU.iloc[i-1, :5].std(ddof=0), 2)
        else:
            print(idx)
    CU.set_index("tmp_idx", inplace=True)
    CU.sort_index(inplace=True)
    CU.set_index("index", inplace=True)
    CU.index.name = "Foil | Section"

    PI = df.copy()
    for idx in PI.index:
        if "CU" in idx:
            PI.drop(labels=idx, inplace=True)
    PI["tmp_idx"] = 0.
    PI["index"] = PI.index
    PI["Mean"] = 0.
    for i, idx in enumerate(PI.index):
        if "Mean" in idx:
            PI.loc[idx, "tmp_idx"] = int(idx.split("_")[0])+0.1
            PI.loc[idx, 'Mean'] = round(PI.iloc[i, :5].mean(), 2)
        elif "Stdev" in idx:
            PI.loc[idx, "tmp_idx"] = int(idx.split("_")[0])+0.2
            PI.loc[idx, 'Mean'] = round(PI.iloc[i-1, :5].std(ddof=0), 2)
        else:
            print(idx)
    PI.set_index("tmp_idx", inplace=True)
    PI.sort_index(inplace=True)
    PI.set_index("index", inplace=True)
    PI.index.name = "Foil | Section"
    return CU, PI


def get_stats(df):
    mean = []
    std = []
    for i, idx in enumerate(df.index):
        if "Mean" in idx:
            mean.append(df.iloc[i, 5])
            std.append(df.iloc[i+1, 5])
        else:
            continue
    assert len(mean) == len(std)

    return mean, std


if __name__ == "__main__":
    sections = ['s1', 's2', 's3', 's4', 's5']
    dirs = [d for d in os.listdir(
        path_data) if "M" in d and len(d.split("_")[-1]) == 5]
    drift_total_ins = {}
    RO_total_ins = {}
    foil_num_list = []
    # create individual plots and store all information to a single dataframe
    for d in dirs:
        info = d.split("_")
        foil_num = int(d[-4:-1])
        foil_num_list.append(foil_num)
        foil_type = "12" if d[-1] == "A" else "3"
        title = f"GE21-FOIL-{info[0]}-G{foil_type}-KR-B{info[1]}-{'0'*(4-len(str(foil_num)))}{foil_num}"
        print(title)
        # read excels
        drift_ins = read_data(pd.read_excel(
            f"{path_data}/{d}/D_Hole_Ins/D_Hole_Diameter_Inspection.xlsx", header=None))
        RO_ins = read_data(pd.read_excel(
            f"{path_data}/{d}/RO_Hole_Ins/RO_Hole_Diameter_Inspection.xlsx", header=None))
        #
        D_Cu_means, D_Cu_stds, D_PI_means, D_PI_stds = analyze(drift_ins)
        RO_Cu_means, RO_Cu_stds, RO_PI_means, RO_PI_stds = analyze(RO_ins)
        drift_total_ins[f"{foil_num}_CUMean"] = D_Cu_means
        drift_total_ins[f"{foil_num}_CUStdev"] = D_Cu_stds
        drift_total_ins[f"{foil_num}_PIMean"] = D_PI_means
        drift_total_ins[f"{foil_num}_PIStdev"] = D_Cu_stds
        RO_total_ins[f"{foil_num}_CUMean"] = RO_Cu_means
        RO_total_ins[f"{foil_num}_CUStdev"] = RO_Cu_stds
        RO_total_ins[f"{foil_num}_PIMean"] = RO_PI_means
        RO_total_ins[f"{foil_num}_PIStdev"] = RO_PI_stds

        fig, ax = plt.subplots()
        plt.errorbar(sections, D_Cu_means, D_Cu_stds, marker="o",
                     color="red", capsize=3, label="Drift Cu mean")
        plt.errorbar(sections, RO_Cu_means, RO_Cu_stds, marker="o",
                     color="blue", capsize=3, label="RO Cu mean")
        plt.errorbar(sections, D_PI_means, D_PI_stds, marker="^",
                     color="red", capsize=3, label="Drift PI mean", mfc="white")
        plt.errorbar(sections, RO_PI_means, RO_PI_stds, marker="^",
                     color="blue", capsize=3, label="RO PI mean", mfc="white")

        plt.xticks(sections)
        plt.title(title)
        plt.xlabel("Section")
        plt.ylabel(r"Mean [$\mu$m]")
        plt.ylim(20, 90)
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig(
            f"{path_saved}/F{'0'*(2-len(str(foil_num)))}{foil_num}_diameter.png")

    dCU, dPI = deco(drift_total_ins)
    rCU, rPI = deco(RO_total_ins)
    dCU.to_excel(f"{path_saved}/Hole_diameter.xlsx",
                 startrow=0, sheet_name="Drift")
    with pd.ExcelWriter(f"{path_saved}/Hole_diameter.xlsx", mode="a", if_sheet_exists="overlay") as writer:
        dPI.to_excel(writer, startrow=len(dCU)+3, sheet_name="Drift")
        rCU.to_excel(writer, startrow=0, sheet_name="RO")
        rPI.to_excel(writer, startrow=len(rCU)+3, sheet_name="RO")

    # draw final plot
    foil_num_list.sort()
    foil_num_list = [str(f) for f in foil_num_list]
    drift_cu_mean, drift_cu_std = get_stats(dCU)
    drift_pi_mean, drift_pi_std = get_stats(dPI)
    ro_cu_mean, ro_cu_std = get_stats(rCU)
    ro_pi_mean, ro_pi_std = get_stats(rPI)

    fig, ax = plt.subplots()
    plt.errorbar(foil_num_list, drift_cu_mean, drift_cu_std,
                 marker="o", color="red", capsize=3, label="Drift Cu mean")
    plt.errorbar(foil_num_list, drift_pi_mean, drift_pi_std,
                 marker="^", color="red", capsize=3, label="Drift PI mean", mfc="white")
    plt.errorbar(foil_num_list, ro_cu_mean, ro_cu_std, marker="o",
                 color="blue", capsize=3, label="RO Cu mean")
    plt.errorbar(foil_num_list, ro_pi_mean, ro_pi_std, marker="^",
                 color="blue", capsize=3, label="RO PI mean", mfc="white")
    plt.title("Hole Diameter Inspection")
    plt.xlabel("Foil Number")
    plt.ylabel(r"Mean [$\mu$m]")
    plt.ylim(20, 90)
    plt.xticks(rotation=45)

    info = 'Foil Type: M{} \nBatch Number: {} \nProduction Site: KR'.format(
        M_type, batch_num)
    props = dict(boxstyle='round', alpha=0.5, ec='gray', fc='white')
    plt.text(0, 26, info, bbox=props)
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(f"{path_saved}/diameter.png")
