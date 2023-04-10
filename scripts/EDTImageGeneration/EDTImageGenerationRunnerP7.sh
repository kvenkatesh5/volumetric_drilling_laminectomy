# Run this from project root
# bash ./scripts/EDTImageGeneration/EDTImageGenerationRunnerP7.sh
mkdir ./resources/edt_grids/spine_P7_256/Vertebral_foramen_256
./build/EDTImageGenerationCmdLine spine_P7 Vertebral_foramen 256
mkdir ./resources/edt_grids/spine_P7_256/L1_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P7 L1_minus_drilling 256
mkdir ./resources/edt_grids/spine_P7_256/L2_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P7 L2_minus_drilling 256
mkdir ./resources/edt_grids/spine_P7_256/L3_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P7 L3_minus_drilling 256
mkdir ./resources/edt_grids/spine_P7_256/L4_minus_drilling_256
./build/EDTImageGenerationCmdLine spine_P7 L4_minus_drilling 256

# combine EDTs
mkdir ./resources/edt_grids/spine_P7_256/L12_minus_drilling_256
mkdir ./resources/edt_grids/spine_P7_256/L23_minus_drilling_256
mkdir ./resources/edt_grids/spine_P7_256/L34_minus_drilling_256
python3 ./scripts/EDTImageGeneration/combine_edt_images.py --input_dir ./resources/edt_grids/spine_P7_256/L1_minus_drilling_256/ --input_dir ./resources/edt_grids/spine_P7_256/L2_minus_drilling_256/ --output_dir ./resources/edt_grids/spine_P7_256/L12_minus_drilling_256/
python3 ./scripts/EDTImageGeneration/combine_edt_images.py --input_dir ./resources/edt_grids/spine_P7_256/L2_minus_drilling_256/ --input_dir ./resources/edt_grids/spine_P7_256/L3_minus_drilling_256/ --output_dir ./resources/edt_grids/spine_P7_256/L23_minus_drilling_256/
python3 ./scripts/EDTImageGeneration/combine_edt_images.py --input_dir ./resources/edt_grids/spine_P7_256/L3_minus_drilling_256/ --input_dir ./resources/edt_grids/spine_P7_256/L4_minus_drilling_256/ --output_dir ./resources/edt_grids/spine_P7_256/L34_minus_drilling_256/