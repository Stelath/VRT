#!/bin/bash

dataset_name=rafting

mkdir benchmark_results

# Do Guassian Noise First
mkdir benchmark_results/"$dataset_name"_guassian_noisy
mkdir benchmark_results/"$dataset_name"_guassian_denoised
for sigma in {5..50..5}
do
    python gen_noisy_frames.py  -f "$dataset_name"/ -o testsets/"$dataset_name"_guassian_noisy/"$dataset_name"_sigma_$sigma -n $sigma -t guassian
    python main_test_vrt.py --task 008_VRT_videodenoising_DAVIS --sigma $sigma --folder_lq testsets/"$dataset_name"_guassian_noisy --tile 12 256 256 --tile_overlap 2 20 20 --save_result
    
    # Move the noisy folder to the corresponding benchmark folder
    mv testsets/"$dataset_name"_guassian_noisy/"$dataset_name"_sigma_$sigma benchmark_results/"$dataset_name"_guassian_noisy/"$dataset_name"_sigma_$sigma

    # Move the output folder to the corresponding benchmark folder
    mv results/008_VRT_videodenoising_DAVIS/"$dataset_name"_sigma_$sigma benchmark_results/"$dataset_name"_guassian_denoised/"$dataset_name"_sigma_$sigma
done

# Do Poisson Noise Next
mkdir benchmark_results/"$dataset_name"_poisson_noisy
mkdir benchmark_results/"$dataset_name"_poisson_denoised
for sigma in {5..50..5}
do
    python gen_noisy_frames.py  -f "$dataset_name"/ -o testsets/"$dataset_name"_poisson_noisy/"$dataset_name"_sigma_conv_$sigma -n $sigma -t poisson -c
    python main_test_vrt.py --task 008_VRT_videodenoising_DAVIS --sigma $sigma --folder_lq testsets/"$dataset_name"_poisson_noisy --tile 12 256 256 --tile_overlap 2 20 20 --save_result
    
    # Move the noisy folder to the corresponding benchmark folder
    mv testsets/"$dataset_name"_poisson_noisy/"$dataset_name"_sigma_conv_$sigma benchmark_results/"$dataset_name"_poisson_noisy/"$dataset_name"_sigma_conv_$sigma

    # Move the output folder to the corresponding benchmark folder
    mv results/008_VRT_videodenoising_DAVIS/"$dataset_name"_sigma_conv_$sigma benchmark_results/"$dataset_name"_poisson_denoised/"$dataset_name"_sigma_conv_$sigma
done

# Do S&P Noise Next
mkdir benchmark_results/"$dataset_name"_sp_noisy
mkdir benchmark_results/"$dataset_name"_sp_denoised
for sigma in {5..50..5}
do
    python gen_noisy_frames.py  -f "$dataset_name"/ -o testsets/"$dataset_name"_sp_noisy/"$dataset_name"_sigma_conv_$sigma -n $sigma -t impulse -c
    python main_test_vrt.py --task 008_VRT_videodenoising_DAVIS --sigma $sigma --folder_lq testsets/"$dataset_name"_sp_noisy --tile 12 256 256 --tile_overlap 2 20 20 --save_result
    
    # Move the noisy folder to the corresponding benchmark folder
    mv testsets/"$dataset_name"_sp_noisy/"$dataset_name"_sigma_conv_$sigma benchmark_results/"$dataset_name"_sp_noisy/"$dataset_name"_sigma_conv_$sigma

    # Move the output folder to the corresponding benchmark folder
    mv results/008_VRT_videodenoising_DAVIS/"$dataset_name"_sigma_conv_$sigma benchmark_results/"$dataset_name"_sp_denoised/"$dataset_name"_sigma_conv_$sigma
done