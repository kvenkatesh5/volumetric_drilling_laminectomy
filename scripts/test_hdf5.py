import numpy as np
import h5py

with h5py.File('test2.hdf5', 'r') as f:
    print(f.keys())
    # voxels_removed
    vx = f["voxels_removed"]
    vxc = vx['voxel_color']
    print(vxc)