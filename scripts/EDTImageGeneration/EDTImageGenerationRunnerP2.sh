# Run this from project root
# bash ./scripts/EDTImageGeneration/EDTImageGenerationRunner.sh
mkdir ./resources/edt_grids/spine_P2_256/Vertebral_foramen_256
./build/EDTImageGenerationCmdLine spine_P2 Vertebral_foramen 256
mkdir ./resources/edt_grids/spine_P2_256/L1_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P2 L1_minus_drilling 256
mkdir ./resources/edt_grids/spine_P2_256/L2_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P2 L2_minus_drilling 256
mkdir ./resources/edt_grids/spine_P2_256/L3_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P2 L3_minus_drilling 256
mkdir ./resources/edt_grids/spine_P2_256/L4_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P2 L4_minus_drilling 256
# mkdir ./resources/edt_grids/spine_P2_256/L1_bottom_boundary_256
# ./build/EDTImageGenerationCmdLine spine_P2 L1_bottom_boundary 256
# mkdir ./resources/edt_grids/spine_P2_256/L2_bottom_boundary_256
# ./build/EDTImageGenerationCmdLine spine_P2 L2_bottom_boundary 256
# mkdir ./resources/edt_grids/spine_P2_256/L3_bottom_boundary_256
# ./build/EDTImageGenerationCmdLine spine_P2 L3_bottom_boundary 256

# combine EDTs
mkdir ./resources/edt_grids/spine_P2_256/L12_minus_drilling_256
mkdir ./resources/edt_grids/spine_P2_256/L23_minus_drilling_256
mkdir ./resources/edt_grids/spine_P2_256/L34_minus_drilling_256
python3 ./scripts/EDTImageGeneration/combine_edt_images.py --input_dir ./resources/edt_grids/spine_P2_256/L1_minus_drilling_256/ --input_dir ./resources/edt_grids/spine_P2_256/L2_minus_drilling_256/ --output_dir ./resources/edt_grids/spine_P2_256/L12_minus_drilling_256/
python3 ./scripts/EDTImageGeneration/combine_edt_images.py --input_dir ./resources/edt_grids/spine_P2_256/L2_minus_drilling_256/ --input_dir ./resources/edt_grids/spine_P2_256/L3_minus_drilling_256/ --output_dir ./resources/edt_grids/spine_P2_256/L23_minus_drilling_256/
python3 ./scripts/EDTImageGeneration/combine_edt_images.py --input_dir ./resources/edt_grids/spine_P2_256/L3_minus_drilling_256/ --input_dir ./resources/edt_grids/spine_P2_256/L4_minus_drilling_256/ --output_dir ./resources/edt_grids/spine_P2_256/L34_minus_drilling_256/