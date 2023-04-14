import numpy as np
#import pptk
from IPython.display import display
import matplotlib.pyplot as plt
import h5py
import open3d as o3d
import pandas as pd
import json
import os
import glob

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

if __name__ == "__main__":
    # read the data in
    #pc_h5 = h5py.File("/home/virtualdrilling/volumetric_drilling/user_study_data/4-6-Testing/klobo-participant/klobo_P0_L1_color/20230406_095631.hdf5", "r")
    pc_h5 = h5py.File("/home/virtualdrilling/volumetric_drilling/user_study_data/4-6-Testing/klobo-participant/klobo_P0_L1_color/20230406_095818.hdf5", "r")
    # look at the voxels_removed group
    voxels_removed_group = pc_h5["voxels_removed"]
    voxels_removed_time_stamp = np.array(voxels_removed_group["voxel_time_stamp"])
    voxels_color = np.array(voxels_removed_group["voxel_color"])
    voxels_removed = np.array(voxels_removed_group["voxel_removed"])
    
    # each of the five columns of the voxel_color represent: index_group of voxel, R, G, B, alpha_value 
    # each index may have multiple voxels removed --> each of the voxel has specified color
    # the colors were all multipled by 255 before beign saved into voxel_color
    print("Color:")
    print(voxels_color)

    # time stamp is each time the removed voxel message shows up at a specific index
    # has time for each index_group (voxels_removed_time_stamp[index_group]) 
    # units in seconds
    print("Time Stamp:")
    print(voxels_removed_time_stamp)

    # each of the four columns of voxels_removed represent: index_group, x, y, z
    # each index may have multiple voxels removed at that time --> each of the voxel has specified position
    print("Voxels Removed Index:")
    print(voxels_removed)
    start_time = voxels_removed_time_stamp[0]
    end_time = voxels_removed_time_stamp[-1] 
    total_time = end_time - start_time
    print(f"Total Drilling Time: {total_time} seconds")
    voxels_removed_time = [(x - start_time) for x in voxels_removed_time_stamp]

    # convert numpy arrays to dataframe (?) for easy analysis
    voxels_color_df = pd.DataFrame(voxels_color, columns = ["Index_Group_of_Voxel", "R", "G", "B", "Alpha_Value"])
    
    # look to see all the unique alpha_values for voxels_color
    unique_alpha = voxels_color_df.Alpha_Value.unique()
    print(unique_alpha)
    
    # alpha_warnings == 0.1, 0.2 --> red
    # alpha_warnings == 0.3 --> yellow
    # alpha_warnings == 1 --> green
    alpha_warnings = [round((x / 255),2) for x in unique_alpha]
    print(alpha_warnings)

    # adjust the Alpha_Value column to match warnings
    voxels_color_df["Alpha_Adjusted"] = voxels_color_df["Alpha_Value"].div(255).round(2)

    # add column for color drilled
    voxels_color_df["Color"] = voxels_color_df.apply(assign_color, axis = 1)

    # add column for time (seconds) drilled
    voxels_color_df["Time(s)"] = voxels_color_df.apply(lambda row : assign_time_group(row["Index_Group_of_Voxel"], voxels_removed_time), axis = 1)
    display(voxels_color_df)



    # add x-y-z coordinates
    

    list_of_index = []
    for i in range(len(voxels_removed)):
        list_of_index.append(voxels_removed[i][0])
    list_of_index = set(list_of_index)  

    giant_list = [] # each index is a time point in list_of_index --> stores voxels removed at that time
    prev_group = 0
    list_at_index = []

    for i in range(len(voxels_removed)):
        group = voxels_removed[i][0]
        if group == prev_group:
            list_at_index.append(voxels_removed[i][1:])
        else:
            giant_list.append(list_at_index)
            list_at_index = []
            list_at_index.append(voxels_removed[i][1:])
            prev_group = group
        if (i == len(voxels_removed) -1):
            giant_list.append(list_at_index)
    print(len(giant_list))

    # this is for viewing the point-cloud stuff --> save for later - Jon
    '''
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    geometry = o3d.geometry.PointCloud()
    points = np.random.rand(10, 3)
    geometry.points = o3d.utility.Vector3dVector(points)
    vis.add_geometry(geometry)
    
    # https://stackoverflow.com/questions/65774814/adding-new-points-to-point-cloud-in-real-time-open3d
    for index in list_of_index:
    # now modify the points of your geometry
    # you can use whatever method suits you best, this is just an example
        intIndex = int(index)
        length = len(giant_list[intIndex])
        pointArray = np.vstack(giant_list[intIndex])
        pointArray.reshape((length, 3))
        #print(pointArray)
        #print("Shape of points: ", pointArray.shape)
        #geometry.points = o3d.utility.Vector3dVector(pointArray)
        geometry.points.extend(pointArray)
        vis.update_geometry(geometry)
        vis.poll_events()
        vis.update_renderer()
        
    # size of voxels_removed_time represents the how long the drill has been removing voxels
    # the first value in a row found in voxels_removed is the index of the time when that voxel was removed (within voxels_removed_time)
    # e.x. if the row is [0, 256, 1, 20], then that voxel was removed at the 0th time value in voxels_removed_time
    # visualize voxels removed
    

    #pptk.viewer(point_clouds[:,0,:,:])
    print("Size of Point Clouds:", point_clouds.shape)
    '''