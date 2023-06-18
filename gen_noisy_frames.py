import os
import argparse
import noise_utils
import numpy as np
from PIL import Image
from tqdm.auto import tqdm

# name mapping

NOISE_NAMES = {
    "guassian": noise_utils.add_guassiannoise,
    "poisson": noise_utils.add_poisson_noise,
    "impulse": noise_utils.add_impulse_noise
}

SUPPORTED_FILE_TYPES = ['.png', '.jpg', '.jpeg']

def is_file_type_supported(file_name):
    """
    Checks if the file type is supported
    """
    return '.' + file_name.split('.')[-1] in SUPPORTED_FILE_TYPES



def main(args):
    """
    Adds noise to all the frames in a video.
    If no type argument is given then all the noise types are used and the results are saved to different folders
    """
    if args.type not in NOISE_NAMES.keys():
        # Will never get called because the argument handler down there is already checking if the argument value is one of the choices
        # But were gonna keep it in cause it makes us feel like we did something
        raise ValueError("ERROR: Noise type given not in NOISE_NAMES:", args.type, "not in", NOISE_NAMES.keys())

    noise_func = NOISE_NAMES[args.type]

    if args.output_folder:
        output_folder = args.output_folder
    else:
        output_folder = args.input_folder + "_" + args.type + "_" + str(args.noise_level).replace(".", "")

    if not os.path.exists(output_folder):
        os.makedirs(args.output_folder)

    
    if args.convert_from_sigma:
        if noise_func == noise_utils.add_guassiannoise:
            print("Warning: There is no reason to convert from sigma if the noise type is already guassian")
        # Taking the first image from their input folder and using it as the base image
        base_image = Image.open(os.path.join(args.file_folder, os.listdir(args.file_folder)[0]))
        base_image = np.asarray(base_image)

        # Using their noise_level as if it were a sigma value for guassian noise and converting it to the noise level for the given noise type
        if noise_func == noise_utils.add_impulse_noise:
            right_extreme = 1
        else:
            right_extreme = 100

        noise_level = noise_utils.get_noise_level_from_g_sigma(noise_func, base_image, args.noise_level, right_extreme)
    else:
        noise_level = args.noise_level

    files = os.listdir(args.file_folder)
    
    # Applying the noise
    for f in tqdm(files):  # Iterating through all the frames in the video
        if is_file_type_supported(f):
            file_type = f.split('.')[-1]
            file_path = os.path.join(args.file_folder, f)
            pil_img = Image.open(file_path)
            img = np.asarray(pil_img)
            pil_img.close()
            noisy_img = noise_func(img, noise_level)
            
            noisy_img = Image.fromarray(noisy_img)
            noisy_img.save(os.path.join(output_folder, f.split('.')[0] + ".png"))
            
    print('noisy frames generated successfully')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file-folder', help='File folder path', required=True)
    parser.add_argument('-o', '--output-folder', help='Output folder path', required=True)
    parser.add_argument('-n',
                        '--noise-level',
                        type=float,
                        help="""The amount of noise to be added to the image, sensitivity varies per type,
                        here are some values for equivilent amounts of noise:
                        Guassian 50
                        Poisson 85
                        Salt and Pepper 12""",
                        required=True)
    parser.add_argument('-c', '--convert-from-sigma',
                        action='store_true',
                        help="""Based on the noise type, calculates a noise-level that results in a similar amount of noise as a guassian noise with the given sigma.
                        Example: If input noise-level is 50 and type is poisson then the noise-level will be converted to 85 to generate a similar amount of noise as sigma 50 with guassian would.""")
    parser.add_argument('-t', '--type', help='Type of the noise being added', choices=list(NOISE_NAMES.keys()), required=True)
    args = parser.parse_args()

    main(args)