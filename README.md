# TODOs
- Resegment spines to represent laminectomy cuts
- Fix the back EDT plane
- Pipeline EDT generation
- Work out issue with seg nrrds ***or move to Henry's plugin

# How to run the pipeline
Let's say we are building P0. Adapt as needed for the other spines.
```
cd ~/volumetric_drilling
bash ./scripts/makeP0pngs.sh
python3 scripts/EdtGeneration/create_all_edt_spine.py --input spine_P0_nocolor_256 --output ./resources/edt_grids/spine_P0_256
bash ./scripts/EDTImageGeneration/EDTImageGenerationRunnerP0.sh
```