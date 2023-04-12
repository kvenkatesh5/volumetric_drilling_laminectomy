import numpy as np
#import pptk
import h5py
import open3d as o3d

if __name__ == "__main__":
    pc_h5 = h5py.File(r"/Users/baby/Desktop/CIS_II_SADGE/20230406_095631.hdf5", "r")
    
    #point_clouds = np.array(pc_h5["data"]["pose_mastoidectomy_volume"])
    point_clouds = np.array(pc_h5["data"]["segm"])
    voxels_removed_time = np.array(pc_h5["voxels_removed"]["voxel_time_stamp"])
    voxels_color = np.array(pc_h5["voxels_removed"]["voxel_color"])
    voxels_removed = np.array(pc_h5["voxels_removed"]["voxel_removed"])
    
    print("Color:")
    print(voxels_color)
    #print("Time:")
    #print(voxels_removed_time)
    #print("Time:", voxels_removed_time.shape)
    #print("Number of voxels_removed:", voxels_removed.shape)

    list_of_index = []
    for i in range(len(voxels_removed)):
        list_of_index.append(voxels_removed[i][0])
    list_of_index = set(list_of_index)  

    giant_list = [] # each index is a time point in list_of_index --> stores voxels removed at that time
    prev_group = 0
    list_at_index = []
    print(voxels_removed[1:5])
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
    '''
    for index in list_of_index:
        list_at_index = []
        for j in range(len(voxels_removed)):
            group = voxels_removed[j][0]
            if (group == index):
                list_at_index.append(voxels_removed[j][1:])
        giant_list.append(list_at_index)
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