# DEVELOPING HDF5 SAVING
# UNDER DEVELOPMENT, USE MAIN FOR USER STUDY

## TODOs
- Resegment spines to represent laminectomy cuts --> DONE
- Fix the back EDT plane --> DONE (implemented the correct EDTs in plugin)
- Pipeline EDT generation --> DONE
- Work out issue with seg nrrds ***or move to Henry's plugin --> DONE

## How to run the pipeline
Let's say we are building P0. Adapt as needed for the other spines.
```
cd ~/volumetric_drilling
bash ./scripts/makeP0pngs.sh
python3 scripts/EdtGeneration/create_all_edt_spine.py --input spine_P0_nocolor_256 --output ./resources/edt_grids/spine_P0_256
bash ./scripts/EDTImageGeneration/EDTImageGenerationRunnerP0.sh
```
