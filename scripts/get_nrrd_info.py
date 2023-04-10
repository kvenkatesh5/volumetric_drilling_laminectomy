import nrrd                                    
import numpy.linalg as la

d, h = nrrd.read("/home/hishida3/Downloads/spine_segmentations/SegmentationP7.seg.nrrd")    
dir = h['space directions']                    

s = h['sizes']                                 

dims = [0, 0, 0]
dims_max = 0
for i in range(3): 
    dims[i]= s[i+1] * la.norm(dir[1:4, i]) 

    if dims_max < dims[i]:
        dims_max = dims[i]

for i in range(3):
    dims[i] = dims[i]/dims_max

print("dim is :", dims)

print("Unit; ", 1.0/dims_max)