import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import torch
import torch.nn as nn
import torch

# Max values for noises
# Guassian 50
# Poisson 85
# Salt and Pepper 12


def get_guassiannoise(data, dist='G', noise_std =50, mode='S', min_noise = 0, max_noise = 55):
    if(dist == 'G'):
        noise_std /= 255.
        min_noise /= 255.
        max_noise /= 255.
        # print(data.shape)
        noise = np.random.randn(*data.shape)
        # noise = torch.randint(data.shape)
        if mode == 'B':
            n = noise.shape[0];
            noise_tensor_array = (max_noise - min_noise) * torch.rand(n) + min_noise;
            for i in range(n):
                noise.data[i] = noise.data[i] * noise_tensor_array[i];
        else:
            noise = noise * noise_std;
    elif(dist == 'P'):
        # noise = torch.randn_like(data);
        noise = np.random.randn(*data.shape)
        if mode == 'S':
            noise_std /= 255.
            # noise = torch.poisson(data*noise_std)/noise_std - data
            noise = np.random.poisson(data*noise_std)/noise_std - data
    return noise

def add_guassiannoise(image, sigma):
    scaled_image = np.copy(image) / 255
    noisy_image = scaled_image + get_guassiannoise(scaled_image, noise_std=sigma)
    noisy_image = (noisy_image * 255)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image


def add_poisson_noise(image, noise_std):
    # Scale the image values to [0, 1]
    image = np.copy(image).astype(np.float32) / 255.0
    noise_std=noise_std/255
    
    # Generate Poisson noise
    noise = np.random.poisson(image * noise_std) / noise_std
    noisy_image = image + noise
    noisy_image = (noisy_image * 255)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    return noisy_image


def add_impulse_noise(image, noise_level):
    if noise_level > 1: noise_level = 1

    # Scale the image values to [0, 1]
    image = np.copy(image).astype(np.float32) / 255.0

    # Generate random noise mask
    mask = np.random.random(image.shape)

    # Set pixels to salt (maximum intensity) noise
    image[mask < noise_level/2] = 1.0

    # Set pixels to pepper (minimum intensity) noise
    image[mask > 1 - noise_level/2] = 0.0

    noisy_image = (image * 255)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    return noisy_image


def get_noise_level_from_g_sigma(noise_func, image, sigma, right_extreme=100):
    """
    Find the noise_level used in the function provided value that would yield and amount of noise
    very close to using a gaussian noise function with the given sigma on the given image
    image: The base image to add noise on for finding the closest value
    sigma: The amount of guassian noise trying to be replicated
    noise_func: Must take in an image and a noise_level and return a noisy image

    Warning: Change right extreme if you are searching for a guassian sigma greater than 100,
    it is set to 100 for performance reasons.
    """

    left = 0
    right = right_extreme
    
    mid = None

    for _ in range(100):
        mid = (left + right) / 2
        diff = 0
        # Taking the average of 10 runs to reduce the effect of randomness from noise generation
        for _ in range(5):
            p_noise_img = noise_func(image, mid)
            g_noise_img = add_guassiannoise(image, sigma)

            p_psnr = peak_signal_noise_ratio(image, p_noise_img)
            g_psnr = peak_signal_noise_ratio(image, g_noise_img)
            diff += p_psnr - g_psnr
        
        diff /= 5

        if abs(diff) < 0.01:
            return mid
        elif diff > 0:
            left = mid
        else:
            right = mid
    print("WARNING: conversion not found in 100 tries")
    return mid


    