import numpy as np
#import pptk
from IPython.display import display
import matplotlib.pyplot as plt
import h5py
# import open3d as o3d
import pandas as pd
import json
import os
import glob
from scipy.stats import ttest_ind
import scipy
import seaborn as sns

def assign_color(data_frame_row):
    alpha_value_adjusted = data_frame_row["Alpha_Adjusted"]
    if alpha_value_adjusted == 1:
        color = "Green"
    elif alpha_value_adjusted == 0.3:
        color = "Yellow"
    else:
        color = "Red"
    return color

def assign_time_group(index_group, voxels_removed_time):
    time = voxels_removed_time[int(index_group)]
    return time

def get_dataframe(filepath, participant, case):
    # read the data in
    pc_h5 = h5py.File(filepath, "r")
    # look at the voxels_removed group
    voxels_removed_group = pc_h5["voxels_removed"]
    try:
        voxels_removed_time_stamp = np.array(voxels_removed_group["voxel_time_stamp"])
        voxels_color = np.array(voxels_removed_group["voxel_color"])
        voxels_removed = np.array(voxels_removed_group["voxel_removed"])
        # print(f"SUCCESS: {participant}_{case}")
    except:
        print(f"ERROR: {filepath} does NOT have the keys requested.")
        return None
    
    # each of the five columns of the voxel_color represent: index_group of voxel, R, G, B, alpha_value 
    # each index may have multiple voxels removed --> each of the voxel has specified color
    # the colors were all multipled by 255 before beign saved into voxel_color
    # print("Color:")
    # print(voxels_color)

    # time stamp is each time the removed voxel message shows up at a specific index
    # has time for each index_group (voxels_removed_time_stamp[index_group]) 
    # units in seconds
    # print("Time Stamp:")
    # print(voxels_removed_time_stamp)

    # each of the four columns of voxels_removed represent: index_group, x, y, z
    # each index may have multiple voxels removed at that time --> each of the voxel has specified position
    # print("Voxels Removed Index:")
    # print(voxels_removed)
    start_time = voxels_removed_time_stamp[0]
    end_time = voxels_removed_time_stamp[-1] 
    total_time = end_time - start_time
    # print(f"Total Drilling Time: {total_time} seconds")
    voxels_removed_time = [(x - start_time) for x in voxels_removed_time_stamp]

    # convert numpy arrays to dataframe (?) for easy analysis
    voxels_color_df = pd.DataFrame(voxels_color, columns = ["Index_Group_of_Voxel", "R", "G", "B", "Alpha_Value"])
    
    # look to see all the unique alpha_values for voxels_color
    unique_alpha = voxels_color_df.Alpha_Value.unique()
    # print(unique_alpha)
    
    # alpha_warnings == 0.1, 0.2 --> red
    # alpha_warnings == 0.3 --> yellow
    # alpha_warnings == 1 --> green
    alpha_warnings = [round((x / 255),2) for x in unique_alpha]
    # print(alpha_warnings)

    # adjust the Alpha_Value column to match warnings
    voxels_color_df["Alpha_Adjusted"] = voxels_color_df["Alpha_Value"].div(255).round(2)

    # add column for color drilled
    voxels_color_df["Color"] = voxels_color_df.apply(assign_color, axis = 1)

    # add column for time (seconds) drilled
    voxels_color_df["Time(s)"] = voxels_color_df.apply(lambda row : assign_time_group(row["Index_Group_of_Voxel"], voxels_removed_time), axis = 1)
    # display(voxels_color_df)

    # return
    return voxels_color_df

def get_drilling_times(all_dfs, participant_list, case_list):
    # return a dictionary with {..., p: {..., (case, drilling_time), ...}, ...}
    drilling_times = dict()

    # for each participant
    for p in participant_list:
        p_drilling_times = dict()
        # for each case
        for c in case_list:
            key = f"{p}_{c}"
            # get all the dataframes for this case
            dataframes = all_dfs[key]
            # get the max times in each dataframe
            t_maxs = [
                np.max(d["Time(s)"]) for d in dataframes
            ]
            # sum these up to get total_time
            total_time = np.sum(np.array(t_maxs))
            # save into a participant dict
            p_drilling_times[c] = total_time
        drilling_times[p] = p_drilling_times
    
    # return
    return drilling_times

def get_nvoxels_removed(all_dfs, voxel_color, participant_list, case_list):
    # return a dictionary with {..., p: {..., (case, nvoxels_removed), ...}, ...}
    nvoxels_removed = dict()

    # for each participant
    for p in participant_list:
        p_nvoxels_removed = dict()
        # for each case
        for c in case_list:
            key = f"{p}_{c}"
            # get all the dataframes for this case
            dataframes = all_dfs[key]
            # count # of voxels of voxel_color per dataframe
            counts = [
                np.sum(d["Color"] == voxel_color) for d in dataframes
            ]
            # total things up
            count = np.sum(counts)
            # save into a participant dict
            p_nvoxels_removed[c] = count
        nvoxels_removed[p] = p_nvoxels_removed
    
    # return
    return nvoxels_removed


if __name__ == "__main__":

    # read json with all the studies listed
    # with open("/home/virtualdrilling/volumetric_drilling/scripts/data_analysis/config.json", "r") as f:
    #     metadata = json.load(f)
    with open("/Users/kesavan/Documents/volumetric_drilling_laminectomy/scripts/data_analysis/config_mac.json", "r") as f:
        metadata = json.load(f)
    
    # all_dfs indexes through all the participants
    all_dfs = dict()

    # for each participant
    for i in range(len(metadata["participants"])):
        p = metadata["participants"][i][0]
        pth = metadata["participants"][i][1]
        # for each case
        for c in metadata["cases"]:
            dirname = os.path.join(pth, f"{p}_{c}")
            # for each hdf5 file
            # FIXED DATA DIRECTORY FORMAT
            filenames = glob.glob(os.path.join(dirname, "*.hdf5"))
            for f in filenames:
                # since there can be multiple filenames per participant-case, we make a list
                key = f"{p}_{c}"
                if key not in all_dfs.keys():
                    all_dfs[key] = []
                df = get_dataframe(f,p,c)
                if df is not None:
                    all_dfs[key].append(df)
                # all_dfs[f"{p}_{c}"] = get_dataframe(f)

    # get time
    participant_list = [x[0] for x in list(metadata["participants"])]
    case_list = list(metadata["cases"])
    is_color_list = [
        False if "no_color" in c else True for c in case_list
    ]
    is_color = {
        case_list[i] : is_color_list[i] for i in range(len(case_list))
    }
    drilling_times = get_drilling_times(all_dfs, participant_list, case_list)
    
    # plot times as boxplots
    drilling_times_plotting = {"NoColor": [], "Color": []}
    for p in participant_list:
        drilling_times_color = []
        drilling_times_nocolor = []
        for c in case_list:
            if is_color[c]:
                drilling_times_color.append(drilling_times[p][c])
            else:
                drilling_times_nocolor.append(drilling_times[p][c])
        drilling_times_plotting["NoColor"].append(np.mean(drilling_times_nocolor))
        drilling_times_plotting["Color"].append(np.mean(drilling_times_color))  
    plt.boxplot(
        [drilling_times_plotting[x] for x in drilling_times_plotting.keys()]
    )
    plt.ylabel("Time (s)")
    plt.xlabel("Condition")
    plt.xticks([1,2], ["NoNav", "ColorNav"])
    # plt.title("Total Drilling Time")
    plt.show()

    # get number of red voxels removed
    red_voxels_removed = get_nvoxels_removed(all_dfs, "Red", participant_list, case_list)
    print(red_voxels_removed)

    # plot red voxels as boxplots
    red_voxels_removed_plotting = {"NoColor": [], "Color": []}
    for p in participant_list:
        red_voxels_removed_color = []
        red_voxels_removed_nocolor = []
        for c in case_list:
            if is_color[c]:
                red_voxels_removed_color.append(red_voxels_removed[p][c])
            else:
                red_voxels_removed_nocolor.append(red_voxels_removed[p][c])
        red_voxels_removed_plotting["NoColor"].append(np.mean(red_voxels_removed_nocolor))
        red_voxels_removed_plotting["Color"].append(np.mean(red_voxels_removed_color))
    sns.boxplot(
        [red_voxels_removed_plotting[x] for x in red_voxels_removed_plotting.keys()],
        width=0.3
    )
    # plt.ylabel("Number of Voxels")
    # plt.xlabel("Condition")
    plt.xticks([0,1], ["NoNav", "ColorNav"])
    # plt.title("Red Voxels Removed")
    plt.show()

    # T-test
    tstat, pval = ttest_ind(red_voxels_removed_plotting["NoColor"], red_voxels_removed_plotting["Color"],
              equal_var=False, random_state=42, alternative="greater")
    print(np.mean(red_voxels_removed_plotting["NoColor"]))
    print(np.mean(red_voxels_removed_plotting["Color"]))
    print(tstat)
    print(pval)
    # F-test
    fstat = np.var(red_voxels_removed_plotting["Color"]) / np.var(red_voxels_removed_plotting["NoColor"])
    dfcolor = len(red_voxels_removed_plotting["Color"])-1
    dfnocolor = len(red_voxels_removed_plotting["NoColor"])-1
    pval = scipy.stats.f.cdf(fstat, dfcolor, dfnocolor)
    print(pval)
