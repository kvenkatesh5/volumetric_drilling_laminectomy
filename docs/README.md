# SDF situational awareness Project

## Overview
The virtual reality drilling simulator is able to modify the anatomy with virtual drill. We create the Signed Distance Field (SDF) girds (.edt format) and present it as image (sdf images).

## 1. Installation instuction
Lets call the absolute location of this package as **<volumetric_plugin_path>**. E.g. if you cloned this repo in your home folder, **<volumetric_plugin_path>** = `~/volumetric_drilling/` OR `/home/<username>/volumetric_plugin`

### 1.1 Install and Source AMBF 2.0

Clone and build `ambf-2.0` branch.
```bash
git clone https://github.com/WPI-AIM/ambf.git
cd ambf
git checkout -b ambf-2.0 origin/ambf-2.0
git pull
```
Note that depth and image recording are enabled by default (in camera ADFs) and these features only work on Linux with ROS installed. Additionally, the following packages must be installed prior to building to AMBF:

```bash
cv-bridge # Can be installed via apt install ros-<version>-cv-bridge
image-transport # Can be installed via apt install ros-<version>-image-transport
```

Build and source ambf (make sure you're on branch ambf-2.0 before building) as per the instructions on AMBFs wiki: https://github.com/WPI-AIM/ambf/wiki/Installing-AMBF.

### 1.2 Install and build EDT directory

Clone and build the `master` branch.

```bash
git clone git@github.com:jabarragann/EDT.git
cd EDT
mkdir cmake-build # Please use thhis exact name for your build folder
cd cmake-build
cmake ..
make 
```



### 1.3 Clone the drilling repo and build

```bash
cd <volumetric_plugin_path>
git clone git@github.com:hisashiishida/volumetric_drilling.git
cd volumetric_drilling 
git checkout sdf_assistance
mkdir build
cd build
cmake ..
make
```

### 1.4 Add another remote to catch up with Adnan's commit
Create a new remote and enable fetching.

```bash
git remote add adnan_repo git@github.com:adnanmunawar/volumetric_drilling.git
git fetch adnan_repo
```

## 2 Generate anatomy and SDF grids
### 2.0 Install required packages

```bash
cd <volumetric_plugin_path> ## change this accroding to your env.
pip install -e . 
pip install -r requirements.txt
```


### 2.1 Create sliced images from the seg.nrrd file
We assume that there is a seg.nrrd file, if not please generate it using 3D slicer (https://www.slicer.org/).
In this readme we assume that seg.nrrd files is in `~/Downloads/spine_segmentations` folder, which contains seg.nrrd files (ex. `SegmentationP0.seg.nrrd` , `SegmentationP7.seg.nrrd`.)


[Warning] Please make sure every structures are colored in a single color. Having two colors will result in blended color in the sliced image.


```bash
cd <volumetric_plugin_path>/scripts
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segmentations/SegmentationP0.seg.nrrd -p ../resources/volumes/spine_P0_256/plane0
```

### 2.2 Create SDF from the sliced image
All the commands in this section should be execute from the project root directory.

Create a txt file with the name of all the images.
```bash
cd <volumetric_plugin_path>
python3 scripts/EdtGeneration/create_list_of_images.py --root ./resources/volumes/spine_p0_256
```

create all spine edt.

```bash
python3 scripts/EdtGeneration/create_all_edt_spine.py --input spine_P0_256 --output resources/edt_grids/spine_P0_256/
```

if the color id is wrong, there gonna be error message during the runtime.

### 2.3 Create SDF-images
Run `EdtImageGeneration` and select the folder name (ex. spine_P0) and structure name (ex. L1_minus drilling), and resolution (ex. 256).

folder name: spine_P0, spine_P1, spine_P2, spine_P4, spine_P7
structure name: L1_minus_drilling, L2_minus_drilling, L3_minus_drilling, Vertebral_foramen

```bash 
cd <volumetric_plugin_path>/build
./EdtImageGeneration
```

### 2.4 Combining the two SDF-images to one
Run python script "combine_edt_images.py" in the script folder.
The input_dir argument is the path to the folder that has SDF images from 2.3.
For example, <input_dir sdf_images path> = "../../resources/edt_grids/spine_P0_256/L1_minus_drilling_256", 

<input_dir sdf_images path2> = "../../resources/edt_grids/spine_P0_256/L2_minus_drilling_256",

<output_dir> = "../../resources/edt_grids/spine_P0_256/L12_minus_drilling_256/"

```
python3 combine_edt_images.py --input_dir <input_dir sdf_images path>  --input_dir <input_dir sdf_images path2> --output_dir <output_dir>
```


### Trouble shooting
If the simulation runs low (~8hz), GPU must be disabled. Please try the following command and make sure ambf process is visble in `nvidia-smi`.

```bash
sudo prime-select nvidia
```


## Actual command used (may need to change the path)

<!-- 
```bash
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP0_separate.seg.nrrd -p ../resources/volumes/spine_P0_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP1_separate.seg.nrrd -p ../resources/volumes/spine_P1_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP2_separate.seg.nrrd -p ../resources/volumes/spine_P2_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP4_separate.seg.nrrd -p ../resources/volumes/spine_P4_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP7_separate.seg.nrrd -p ../resources/volumes/spine_P7_256/plane0


python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP0_vis.seg.nrrd -p ../resources/volumes/spine_P0_visual_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP1_vis.seg.nrrd -p ../resources/volumes/spine_P1_visual_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP2_vis.seg.nrrd -p ../resources/volumes/spine_P2_visual_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP4_vis.seg.nrrd -p ../resources/volumes/spine_P4_visual_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/spine_segments_1205/SegmentationP7_vis.seg.nrrd -p ../resources/volumes/spine_P7_visual_256/plane0


python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P0_test_segments/segmentP0_L1_color_test.seg.nrrd -p ../resources/volumes/spine_P0_L1_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P0_test_segments/segmentP0_L1_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P0_L1_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P0_test_segments/segmentP0_L2_color_test.seg.nrrd -p ../resources/volumes/spine_P0_L2_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P0_test_segments/segmentP0_L2_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P0_L2_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P0_test_segments/segmentP0_L3_color_test.seg.nrrd -p ../resources/volumes/spine_P0_L3_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P0_test_segments/segmentP0_L3_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P0_L3_nocolor_256/plane0

python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P1_test_segments/segmentP1_L1_color_test.seg.nrrd -p ../resources/volumes/spine_P1_L1_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P1_test_segments/segmentP1_L1_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P1_L1_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P1_test_segments/segmentP1_L2_color_test.seg.nrrd -p ../resources/volumes/spine_P1_L2_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P1_test_segments/segmentP1_L2_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P1_L2_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P1_test_segments/segmentP1_L3_color_test.seg.nrrd -p ../resources/volumes/spine_P1_L3_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P1_test_segments/segmentP1_L3_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P1_L3_nocolor_256/plane0

python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P2_test_segments/segmentP2_L1_color_test.seg.nrrd -p ../resources/volumes/spine_P2_L1_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P2_test_segments/segmentP2_L1_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P2_L1_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P2_test_segments/segmentP2_L2_color_test.seg.nrrd -p ../resources/volumes/spine_P2_L2_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P2_test_segments/segmentP2_L2_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P2_L2_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P2_test_segments/segmentP2_L3_color_test.seg.nrrd -p ../resources/volumes/spine_P2_L3_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P2_test_segments/segmentP2_L3_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P2_L3_nocolor_256/plane0

python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P4_test_segments/segmentP4_L1_color_test.seg.nrrd -p ../resources/volumes/spine_P4_L1_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P4_test_segments/segmentP4_L1_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P4_L1_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P4_test_segments/segmentP4_L2_color_test.seg.nrrd -p ../resources/volumes/spine_P4_L2_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P4_test_segments/segmentP4_L2_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P4_L2_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P4_test_segments/segmentP4_L3_color_test.seg.nrrd -p ../resources/volumes/spine_P4_L3_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P4_test_segments/segmentP4_L3_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P4_L3_nocolor_256/plane0

python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P7_test_segments/segmentP7_L1_color_test.seg.nrrd -p ../resources/volumes/spine_P7_L1_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P7_test_segments/segmentP7_L1_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P7_L1_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P7_test_segments/segmentP7_L2_color_test.seg.nrrd -p ../resources/volumes/spine_P7_L2_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P7_test_segments/segmentP7_L2_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P7_L2_nocolor_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P7_test_segments/segmentP7_L3_color_test.seg.nrrd -p ../resources/volumes/spine_P7_L3_color_256/plane0
python3 seg_nrrd_to_pngs.py -n ~/Downloads/test_segments/P7_test_segments/segmentP7_L3_nocolor_test.seg.nrrd -p ../resources/volumes/spine_P7_L3_nocolor_256/plane0
```
 -->






