#!/bin/bash

for sigma in {5..50..5}  # the third 10 is the step size
do
    python main_test_vrt.py --task 008_VRT_videodenoising_DAVIS --sigma $sigma --folder_lq testsets/MedSet --tile 12 256 256 --tile_overlap 2 20 20 --save_result
    
    # Rename the output folder to the corresponding sigma
    mv results/008_VRT_videodenoising_DAVIS/MUSC1 results/MUSCTestRuns/MUSC1_$sigma
    mv results/008_VRT_videodenoising_DAVIS/MUSC2 results/MUSCTestRuns/MUSC2_$sigma
done
