import json
import h5py
import numpy as np

# with open("./data_analysis/config.json") as j:
#     config = json.load(j)

data = h5py.File("/home/virtualdrilling/Volumetric Drilling Userstudy/4-6-Testing/klobo-participant/klobo_P1_L1_no_color/20230406_102149.hdf5", "r")

print(data.keys())
print(data["metadata"].keys())
print(data["metadata"]["README"])
print(data["voxels_removed"].keys())
c = data["voxels_removed"]["voxel_color"]
c = np.array(c)
print(c.shape)
for i in range(5):
    print(c[i][1:])
v = data["voxels_removed"]["voxel_removed"]
v = np.array(v)
for j in range(5):
    print(v[j])
t = data["voxels_removed"]["voxel_time_stamp"]
t = np.array(t)
for k in range(5):
    print(t[k])
print(t[-1])
print(t[-1]-t[0])
# what units are these time stamps in?
